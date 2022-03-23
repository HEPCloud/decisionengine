# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import re

import redis

from kombu.transport.redis import Channel


def redis_stats(broker_url, exchange):
    r = redis.Redis.from_url(broker_url)
    queue_to_routing_key = {}
    # The exchange name is prefixed by a Kombu-provided pattern
    for member in r.smembers(Channel.keyprefix_queue % exchange):
        matches = re.fullmatch(b"^(.*?)\x06.*\x16(.*)$", member)
        queue_to_routing_key[matches[2].decode()] = matches[1].decode()

    result = []
    for queue_name, routing_key in queue_to_routing_key.items():
        rtype = r.type(queue_name).decode()
        if rtype == "none":
            result.append([routing_key, queue_name, "None"])
        elif rtype != "list":
            result.append([routing_key, queue_name, "Unsupported"])
        else:
            result.append([routing_key, queue_name, f"{r.llen(queue_name)}"])

    result.sort()  # Sort in alphabetical order according to routing key
    return result
