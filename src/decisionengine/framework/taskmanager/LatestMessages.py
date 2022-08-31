# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""The LatestMessages class listens for messages from a set of queues and
retains only the last unconsumed message from each queue.

The latest messages are consumed by calling the consume() instance
method, which returns a dictionary whose key is the message routing
key and whose value is the full message.  If no messages are
available, consume() returns an empty dictionary.

The LatestMessages class is intended to be used as a context manager (e.g.):

.. code-block:: python

    with LatestMessages(queues, broker_url) as messages:
        while some_predicate():
            msgs = messages.consume()
            if not msgs:
                continue

            for routing_key, msg in msgs.items():
                ...

Upon exiting the the context, a LatestMessage object will no longer
listen for any messages.
"""

import copy
import socket
import threading

from kombu import Connection
from kombu.pools import connections


class LatestMessages:
    def __init__(self, queues, broker_url):
        self._listening = threading.Event()
        self._msglock = threading.Lock()
        self._messages = {}
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._listen)
        self.queues = queues
        self.broker_url = broker_url

    def consume(self):
        "Return dictionary of latest messages, keyed by message routing key."
        with self._msglock:
            if self._messages:
                msgs = copy.deepcopy(self._messages)
                self._messages.clear()
                return msgs
        return {}

    def __enter__(self):
        self._thread.start()
        self._listening.wait()
        return self

    def __exit__(self, type, value, traceback):
        self._stop.set()
        self._thread.join()

    def _listen(self):
        def receive(body, message):
            with self._msglock:
                routing_key = message.delivery_info["routing_key"]
                self._messages[routing_key] = body
                message.ack()

        _cl = Connection(self.broker_url)
        with connections[_cl].acquire(block=True) as conn, conn.Consumer(
            self.queues, accept=["pickle"], callbacks=[receive]
        ):
            self._listening.set()
            while not self._stop.is_set():
                try:
                    # If source has been brought offline while the drain_events method is
                    # executing, it will stall.  We therefore impose an arbitrary 5-second
                    # timeout so that the 'should_stop()' method called in the while condition
                    # will yield false and thus terminate the loop.
                    conn.drain_events(timeout=5)
                except (TimeoutError, socket.timeout):
                    # no events found in time
                    pass
