# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import logging
import socket
import sys

from kombu import Connection, Exchange, Queue


class ClientMessageReceiver:
    def __init__(self, exchange_name, exchange_type, broker_url, routing_key_suffix, logger_name):
        self._broker_url = broker_url
        self._exchange = Exchange(exchange_name, exchange_type)
        self._queue = Queue(
            f"client.requests.listener.{routing_key_suffix}",
            exchange=self._exchange,
            routing_key=f"client.requests.{routing_key_suffix}",
            auto_delete=True,
        )
        self._done = False
        self._logger = None
        self._text = None
        if logger_name is not None:
            self._logger = logging.getLogger(logger_name)
            self._logger.setLevel(logging.INFO)
            self._logger.addHandler(logging.StreamHandler(sys.stdout))
        else:
            self._text = ""

    def _receive(self, body, message):
        # None is used to indicate the end of the message from the DE server
        if body is None:
            self._done = True
            message.ack()
            return
        if isinstance(body, bytes):
            body = body.decode()
        if self._text is not None:
            self._text += body
        else:
            assert self._logger is not None
            self._logger.info(body)
        message.ack()

    def execute(self, func, *args):
        with Connection(self._broker_url) as conn, conn.Consumer([self._queue], callbacks=[self._receive]):
            func(*args)
            while not self._done:
                try:
                    conn.drain_events(timeout=2)
                except (TimeoutError, socket.timeout):  # pragma: no cover
                    # no events found in time
                    pass
            self._queue.bind(conn.channel()).purge()
        return self._text
