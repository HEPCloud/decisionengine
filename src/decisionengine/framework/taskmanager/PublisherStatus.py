# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""PublisherStatus

The status of each decision-engine publisher is captured by a PublisherStatus object.
The status can be queried to determine if a given publisher is enabled, and when it was last
enabled or disabled.  To access this information from a datablock, one must specify the
a consumes statement:

..  code_block:: python
    @Transform.consumes(publisher_status=PublisherStatus)
    class MyTransform(Transform.Transform):
        ...
        def transform(self, datablock):
            status = self.publisher_status(datablock)

            if status.is_enabled("some_publisher"):
                # some_publisher is enabled
                ...
            elif status.state("some_publisher").duration.seconds > 10:
                # some_publisher has been disabled for at least 10 seconds
                ...

The API for each relevant class is given below.
"""

from datetime import datetime, timedelta
from typing import NamedTuple

from tabulate import tabulate


class PublisherState(NamedTuple):
    enabled: bool
    duration: timedelta
    since: datetime


PublisherState.enabled.__doc__ = "Boolean value indicating if publisher is enabled."
PublisherState.duration.__doc__ = (
    "datetime.timedelta object representing duration between now and when publisher was last enabled/disabled"
)
PublisherState.since.__doc__ = "datetime.datetime object representing when publisher was last enabled/disabled"


class PublisherStatus:
    """Proxy object that provides publisher-status information."""

    def __init__(self, status_snapshot):
        self._status = status_snapshot

    def is_enabled(self, publisher_name):
        """
        :param str publisher_name: The name of the configured publisher
        :return: If publisher is enabled or disabled
        :rtype: bool
        """
        return self._status[publisher_name][0]

    def state(self, publisher_name):
        """
        :param str publisher_name: The name of the configured publisher
        :return: Full state of publisher
        :rtype: :class:`PublisherState`
        """
        is_enabled, time_of_update = self._status[publisher_name]
        return PublisherState(enabled=is_enabled, duration=datetime.now() - time_of_update, since=time_of_update)

    def __str__(self):
        return tabulate([(k,) + v for k, v in self._status.items()], headers=["Publisher", "Enabled", "Since"])


class PublisherStatusBoard:
    """Publisher status board owned by each decision channel

    The status board is not a user-facing entity; it is owned by each decision
    channel, which updates the status of each publisher after they have been run.
    """

    def __init__(self, publisher_names):
        # All publishers are enabled by default
        self._status = dict.fromkeys(publisher_names, (True, datetime.now()))

    def update(self, publisher_name, result_of_publish):
        """
        :param str publisher_name: The name of the configured publisher
        :param bool result_of_publish: Whether the last execution of the publisher was successsul
        """
        # It is a logical error to call update on a publisher whose
        # name has not been specified in the constructor.
        assert publisher_name in self._status

        # Do not update the status of the publisher if the cached
        # status is the same as result_of_publish
        if self._status.get(publisher_name)[0] == result_of_publish:
            return

        self._status[publisher_name] = (result_of_publish, datetime.now())

    def snapshot(self):
        """
        :return: An publisher-status object corresponding to now
        :rtype: :class:`PublisherStatus`
        """
        return PublisherStatus(self._status)
