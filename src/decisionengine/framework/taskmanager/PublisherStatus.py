# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from collections import namedtuple
from datetime import datetime

from tabulate import tabulate

PublisherState = namedtuple("PublisherState", ["enabled", "duration", "since"])


class PublisherStatus:
    def __init__(self, status_snapshot):
        self._status = status_snapshot

    def is_enabled(self, publisher_name):
        return self._status[publisher_name][0]

    def status(self, publisher_name):
        is_enabled, time_of_update = self._status[publisher_name]
        return PublisherState(enabled=is_enabled, duration=datetime.now() - time_of_update, since=time_of_update)

    def __str__(self):
        return tabulate([(k,) + v for k, v in self._status.items()], headers=["Publisher", "Enabled", "Since"])


class PublisherStatusBoard:
    def __init__(self, publisher_names):
        # All publishers are enabled by default
        self._status = dict.fromkeys(publisher_names, (True, datetime.now()))

    def update(self, publisher_name, result_of_publish):
        # It is a logical error to call update on a publisher whose
        # name has not been specified in the constructor.
        assert publisher_name in self._status

        # Do not update the status of the publisher if the cached
        # status is the same as result_of_publish
        if self._status.get(publisher_name)[0] == result_of_publish:
            return

        self._status[publisher_name] = (result_of_publish, datetime.now())

    def snapshot(self):
        return PublisherStatus(self._status)
