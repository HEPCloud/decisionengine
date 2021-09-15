"""
Decision Engine ComponentManager
(Base class for ChannelManager and SourceManager)
"""

#import importlib # Disabled until it is needed by SourceManager and ChannelManager
import logging
import multiprocessing
import uuid

from decisionengine.framework.dataspace import dataspace
from decisionengine.framework.dataspace import datablock
from decisionengine.framework.taskmanager.ProcessingState import State, ProcessingState

# Disabled until it is needed by SourceManager and ChannelManager
#def create_runner(module_name, class_name, parameters):
#    """
#    Create instance of dynamically loaded module
#    """
#    my_module = importlib.import_module(module_name)
#    class_type = getattr(my_module, class_name)
#    return class_type(parameters)


class ComponentManager:
    """
    Base class for decisionengine components such as Sources and Channels
    """

    def __init__(self, name, generation_id, global_config):
        """
        :type name: :obj:`str`
        :arg name: Name of source corresponding to this source manager
        :type generation_id: :obj:`int`
        :arg generation_id: Source Manager generation id provided by caller
        :type global_config: :obj:`dict`
        :arg global_config: global configuration
         """
        self.id = str(uuid.uuid4()).upper()
        self.dataspace = dataspace.DataSpace(global_config)
        self.data_block_t0 = datablock.DataBlock(self.dataspace,
                                                 name,
                                                 self.id,
                                                 generation_id)  # my current data block
        self.name = name
        self.state = ProcessingState()
        self.loglevel = multiprocessing.Value('i', logging.WARNING)

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

    def data_block_put(self, data, header, data_block):
        """
        Put data into data block

        :type data: :obj:`dict`
        :arg data: key, value pairs
        :type header: :obj:`~datablock.Header`
        :arg header: data header
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """

        if not isinstance(data, dict):
            logging.getLogger().error(f'data_block put expecting {dict} type, got {type(data)}')
            return
        logging.getLogger().debug(f'data_block_put {data}')
        with data_block.lock:
            # This is too long to find, so im leaving it here to make it obvious whats going on
            #   you'll want to update it eventually.
            #metadata = datablock.Metadata(data_block.component_manager_id,
            metadata = datablock.Metadata(data_block.taskmanager_id,
                                          state='END_CYCLE',
                                          generation_id=data_block.generation_id)
            for key, product in data.items():
                data_block.put(key, product, header, metadata=metadata)

    def take_offline(self, current_data_block):
        """
        offline and stop this component manager
        """
        self.state.set(State.OFFLINE)
        # invalidate data block
        # not implemented yet
