# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0


class PublisherStatus:
    def __init__(self, publisher_names):
        # All publishers are enabled by default
        self._enabled = dict.fromkeys(publisher_names, True)

    def update(self, publisher_name, result_of_publish):
        # It is a logical error to call update on a publisher whose
        # name has not been specified in the constructor.
        assert publisher_name in self.enabled
        self._enabled[publisher_name] = result_of_publish

    def is_enabled(self, publisher_name):
        return self._enabled[publisher_name]
