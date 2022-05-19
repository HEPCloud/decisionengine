# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import threading
import time

from concurrent.futures import ThreadPoolExecutor, wait

import redis

from kombu import Connection, Exchange, Queue
from kombu.pools import producers

from decisionengine.framework.taskmanager.LatestMessages import LatestMessages

_BROKER_URL = "redis://localhost:6379/15"  # Use 15 to avoid collisions with other tests
_EXCHANGE = Exchange("test_topic_exchange", "topic")


def message(source, msg_count):
    return f"Message {msg_count} for {source}"


def simple_listen(sources, barrier):
    queues_for_receiving = [Queue(name, exchange=_EXCHANGE, routing_key=name, auto_delete=True) for name in sources]
    with LatestMessages(queues_for_receiving, _BROKER_URL) as messages:
        # Do not consume messages until all senders have finished sending their messages
        barrier.wait()
        return messages.consume()


def send_messages(name, num_messages, barrier):
    queue = Queue(name, exchange=_EXCHANGE, routing_key=name, auto_delete=True)
    con = Connection(_BROKER_URL)
    sleep_for = 10 / num_messages  # Send enough messages to consume 10 seconds
    with producers[con].acquire(block=True) as producer:
        for i in range(num_messages):
            producer.publish(
                message(name, i + 1),
                routing_key=name,
                exchange=_EXCHANGE,
                serializer="pickle",
                declare=[_EXCHANGE, queue],
            )
            time.sleep(sleep_for)
    barrier.wait()


# Test that for 3 queues sending messages at different rates, the
# LatestMessages class correctly retains only the latest one.  To do
# this, we check that the "consume()" instance method returns only the
# last message per queue after all of the messages have been sent.
def test_latest_messages():
    sources = {"source1": 10, "source2": 5, "source3": 2}
    barrier = threading.Barrier(len(sources) + 1)  # The "+ 1" is for the listener
    ref = {name: message(name, num_messages) for name, num_messages in sources.items()}
    with ThreadPoolExecutor() as ex:
        msgs = ex.submit(simple_listen, sources, barrier)
        senders = [ex.submit(send_messages, name, num_messages, barrier) for name, num_messages in sources.items()]
        wait(senders)
        assert msgs.result() == ref
    redis.Redis.from_url(_BROKER_URL).flushdb()
