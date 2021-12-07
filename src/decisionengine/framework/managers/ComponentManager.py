# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Decision Engine ComponentManager
(Base class for ChannelManager and SourceManager)
"""

import logging
import multiprocessing

from decisionengine.framework.taskmanager.ProcessingState import ProcessingState, State


class ComponentManager:
    """
    Base class for decisionengine components such as Sources and Channels
    """

    def __init__(self, name):
        """
        :type name: :obj:`str`
        :arg name: Name of source corresponding to this source manager
        """
        self.name = name
        self.state = ProcessingState()
        self.loglevel = multiprocessing.Value("i", logging.WARNING)

    def get_state_value(self):
        return self.state.get_state_value()

    def get_state(self):
        return self.state.get()

    def get_state_name(self):
        return self.get_state().name

    def set_loglevel_value(self, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        with self.loglevel.get_lock():
            # Convert from string to int form using technique
            # suggested by logging module
            self.loglevel.value = getattr(logging, log_level)

    def get_loglevel(self):
        with self.loglevel.get_lock():
            return self.loglevel.value

    def take_offline(self):
        """
        Adjust status to offline
        """
        self.state.set(State.OFFLINE)
