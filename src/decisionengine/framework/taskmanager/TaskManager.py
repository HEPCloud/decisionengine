"""
Task Manager
"""
import importlib
import threading
import logging
import time
import multiprocessing
import uuid

import pandas

from decisionengine.framework.dataspace import dataspace
from decisionengine.framework.dataspace import datablock
from decisionengine.framework.taskmanager.ProcessingState import State
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState

_TRANSFORMS_TO = 300  # 5 minutes
_DEFAULT_SCHEDULE = 300  # ""


def _create_worker(module_name, class_name, parameters):
    """
    Create instance of dynamically loaded module
    """
    my_module = importlib.import_module(module_name)
    class_type = getattr(my_module, class_name)
    return class_type(parameters)


class Worker:
    """
    Provides interface to loadable modules an events to sycronise
    execution
    """

    def __init__(self, conf_dict):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the worker
        """

        self.worker = _create_worker(conf_dict['module'],
                                     conf_dict['name'],
                                     conf_dict['parameters'])
        self.module = conf_dict['module']
        self.name = self.worker.__class__.__name__
        self.schedule = conf_dict.get('schedule', _DEFAULT_SCHEDULE)
        self.run_counter = 0
        self.data_updated = threading.Event()
        self.stop_running = threading.Event()
        logging.getLogger("decision_engine").debug('Creating worker: module=%s name=%s parameters=%s schedule=%s',
                                                   self.module, self.name, conf_dict['parameters'], self.schedule)


def _make_workers_for(configs):
    return {name: Worker(e) for name, e in configs.items()}


class Channel:
    """
    Decision Channel.
    Instantiates workers according to channel configuration
    """

    def __init__(self, channel_dict):
        """
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        """

        logging.getLogger("decision_engine").debug('Creating channel source')
        self.sources = _make_workers_for(channel_dict['sources'])
        logging.getLogger("decision_engine").debug('Creating channel transform')
        self.transforms = _make_workers_for(channel_dict['transforms'])
        logging.getLogger("decision_engine").debug('Creating channel logicengine')
        self.le_s = _make_workers_for(channel_dict['logicengines'])
        logging.getLogger("decision_engine").debug('Creating channel publisher')
        self.publishers = _make_workers_for(channel_dict['publishers'])
        self.task_manager = channel_dict.get('task_manager', {})


class TaskManager:
    """
    Task Manager
    """

    def __init__(self, name, generation_id, channel_dict, global_config):
        """
        :type name: :obj:`str`
        :arg name: Name of channel corresponding to this task manager
        :type generation_id: :obj:`int`
        :arg generation_id: Task Manager generation id provided by caller
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
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
        self.channel = Channel(channel_dict)
        self.state = ProcessingState()
        self.loglevel = multiprocessing.Value('i', logging.WARNING)
        self.lock = threading.Lock()
        # The rest of this function will go away once the source-proxy
        # has been reimplemented.
        for src_worker in self.channel.sources.values():
            src_worker.worker.post_create(global_config)

    def wait_for_all(self, events_done):
        """
        Wait for all sources or transforms to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        logging.getLogger().info('Waiting for all tasks to run')

        try:
            while not all([e.is_set() for e in events_done]):
                time.sleep(1)
                if self.state.should_stop():
                    break

            for e in events_done:
                e.clear()
        except Exception:  # pragma: no cover
            logging.getLogger().exception("Unexpected error!")
            raise

    def wait_for_any(self, events_done):
        """
        Wait for any sources to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        try:
            while not any([e.is_set() for e in events_done]):
                time.sleep(1)
                if self.state.should_stop():
                    break

            for e in events_done:
                if e.is_set():
                    e.clear()
        except Exception:  # pragma: no cover
            logging.getLogger().exception("Unexpected error!")
            raise

    def run(self):
        """
        Task Manager main loop
        """
        logging.getLogger().setLevel(self.loglevel.value)
        logging.getLogger().info(f'Starting Task Manager {self.id}')
        done_events, source_threads = self.start_sources(self.data_block_t0)
        # This is a boot phase
        # Wait until all sources run at least one time
        self.wait_for_all(done_events)
        logging.getLogger().info('All sources finished')
        if not self.state.has_value(State.BOOT):
            for thread in source_threads:
                thread.join()
            logging.getLogger().error(
                f'Error occured during initial run of sources. Task Manager {self.name} exits')
            return

        self.decision_cycle()
        self.state.set(State.STEADY)

        while not self.state.should_stop():
            try:
                self.wait_for_any(done_events)
                self.decision_cycle()
                if self.state.should_stop():
                    logging.getLogger().info(f'Task Manager {self.id} received stop signal and exits')
                    for source in self.channel.sources.values():
                        source.stop_running.set()
                        time.sleep(5)
                    for transform in self.channel.transforms.values():
                        transform.stop_running.set()
                        time.sleep(5)
                    break
            except Exception:  # pragma: no cover
                logging.getLogger().exception("Exception in the task manager main loop")
                logging.getLogger().error('Error occured. Task Manager %s exits with state %s',
                                          self.id, self.get_state_name())
                break
            time.sleep(1)
        for thread in source_threads:
            thread.join()

    def get_state_value(self):
        with self.state.get_lock():
            return self.state.value

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

    def take_offline(self, current_data_block):
        """
        offline and stop task manager
        """
        self.state.set(State.OFFLINE)
        # invalidate data block
        # not implemented yet

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
            metadata = datablock.Metadata(data_block.taskmanager_id,
                                          state='END_CYCLE',
                                          generation_id=data_block.generation_id)
            for key, product in data.items():
                data_block.put(key, product, header, metadata=metadata)

    def do_backup(self):
        """
        Duplicate current data block and return its copy

        :rtype: :obj:`~datablock.DataBlock`

        """

        with self.lock:
            data_block = self.data_block_t0.duplicate()
            logging.getLogger().debug(f'Duplicated block {data_block}')
        return data_block

    def decision_cycle(self):
        """
        Decision cycle to be run periodically (by trigger)
        """

        data_block_t1 = self.do_backup()
        try:
            self.run_transforms(data_block_t1)
        except Exception:
            logging.getLogger().exception("error in decision cycle(transforms) ")
            # We do not call 'take_offline' here because it has
            # already been called in the run_transform code on
            # operating on a separate thread.

        actions_facts = []
        try:
            actions_facts = self.run_logic_engine(data_block_t1)
            logging.getLogger().info('ran all logic engines')
        except Exception:
            logging.getLogger().exception("error in decision cycle(logic engine) ")
            self.take_offline(data_block_t1)

        for a_f in actions_facts:
            try:
                self.run_publishers(
                    a_f['actions'], a_f['newfacts'], data_block_t1)
            except Exception:
                logging.getLogger().exception("error in decision cycle(publishers) ")
                self.take_offline(data_block_t1)

    def run_source(self, src):
        """
        Get the data from source
        and put it into the data block

        :type src: :obj:`~Worker`
        :arg src: source Worker
        """

        # If task manager is in offline state, do not keep executing sources.
        while not self.state.should_stop():
            try:
                logging.getLogger().info(f'Src {src.name} calling acquire')
                data = src.worker.acquire()
                logging.getLogger().info(f'Src {src.name} acquire retuned')
                logging.getLogger().info(f'Src {src.name} filling header')
                if data:
                    t = time.time()
                    header = datablock.Header(self.data_block_t0.taskmanager_id,
                                              create_time=t, creator=src.module)
                    logging.getLogger().info(f'Src {src.name} header done')
                    self.data_block_put(data, header, self.data_block_t0)
                    logging.getLogger().info(f'Src {src.name} data block put done')
                else:
                    logging.getLogger().warning(f'Src {src.name} acquire retuned no data')
                src.run_counter += 1
                src.data_updated.set()
                logging.getLogger().info(f'Src {src.name} {src.module} finished cycle')
            except Exception:
                logging.getLogger().exception(f'Exception running source {src.name} ')
                self.take_offline(self.data_block_t0)
            if src.schedule > 0:
                s = src.stop_running.wait(src.schedule)
                if s:
                    logging.getLogger().info(f'received stop_running signal for {src.name}')
                    break
            else:
                logging.getLogger().info(f'source {src.name} runs only once')
                break
        logging.getLogger().info(f'stopped {src.name}')

    def start_sources(self, data_block=None):
        """
        Start sources, each in a separate thread

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """

        event_list = []
        source_threads = []

        for key, source in self.channel.sources.items():
            logging.getLogger().info(f'starting loop for {key}')
            event_list.append(source.data_updated)
            thread = threading.Thread(target=self.run_source,
                                      name=source.name,
                                      args=(source,))
            source_threads.append(thread)
            # Cannot catch exception from function called in separate thread
            thread.start()
        return (event_list, source_threads)

    def run_transforms(self, data_block=None):
        """
        Run transforms.
        So far in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        logging.getLogger().info('run_transforms')
        logging.getLogger().debug(f'run_transforms: data block {data_block}')
        if not data_block:
            return
        event_list = []
        threads = []
        for key, transform in self.channel.transforms.items():
            logging.getLogger().info(f'starting transform {key}')
            event_list.append(transform.data_updated)
            thread = threading.Thread(target=self.run_transform,
                                      name=transform.name,
                                      args=(transform, data_block))
            threads.append(thread)
            # Cannot catch exception from function called in separate thread
            thread.start()

        self.wait_for_all(event_list)
        for thread in threads:
            thread.join()
        logging.getLogger().info('all transforms finished')

    def run_transform(self, transform, data_block):
        """
        Run a transform

        :type transform: :obj:`~Worker`
        :arg transform: source Worker
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        data_to = self.channel.task_manager.get('data_TO', _TRANSFORMS_TO)
        consume_keys = transform.worker.consumes()

        logging.getLogger().info('transform: %s expected keys: %s provided keys: %s',
                                 transform.name, consume_keys, list(data_block.keys()))
        loop_counter = 0
        while not self.state.should_stop():
            # Check if data is ready
            if set(consume_keys) <= set(data_block.keys()):
                # data is ready -  may run transform()
                logging.getLogger().info('run transform %s', transform.name)
                try:
                    with data_block.lock:
                        data = transform.worker.transform(data_block)
                    logging.getLogger().debug(f'transform returned {data}')
                    t = time.time()
                    header = datablock.Header(data_block.taskmanager_id,
                                              create_time=t,
                                              creator=transform.name)
                    self.data_block_put(data, header, data_block)
                    logging.getLogger().info('transform put data')
                except Exception:
                    logging.getLogger().exception(f'exception from transform {transform.name} ')
                    self.take_offline(data_block)
                break
            s = transform.stop_running.wait(1)
            if s:
                logging.getLogger().info(f'received stop_running signal for {transform.name}')
                break
            loop_counter += 1
            if loop_counter == data_to:
                logging.getLogger().info(f'transform {transform.name} did not get consumes data'
                                         f'in {data_to} seconds. Exiting')
                break
        transform.data_updated.set()

    def run_logic_engine(self, data_block=None):
        """
        Run Logic Engine.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        le_list = []
        if not data_block:
            return

        try:
            for le in self.channel.le_s:
                logging.getLogger().info('run logic engine %s',
                                         self.channel.le_s[le].name)
                logging.getLogger().debug('run logic engine %s %s',
                                          self.channel.le_s[le].name, data_block)
                rc = self.channel.le_s[le].worker.evaluate(data_block)
                le_list.append(rc)
                logging.getLogger().info('run logic engine %s done',
                                         self.channel.le_s[le].name)
                logging.getLogger().info('logic engine %s generated newfacts: %s',
                                         self.channel.le_s[le].name, rc['newfacts'].to_dict(orient='records'))
                logging.getLogger().info('logic engine %s generated actions: %s',
                                         self.channel.le_s[le].name, rc['actions'])

            # Add new facts to the datablock
            # Add empty dataframe if nothing is available
            if le_list:
                all_facts = pandas.concat([i['newfacts']
                                           for i in le_list], ignore_index=True)
            else:
                logging.getLogger().info('Logic engine(s) did not return any new facts')
                all_facts = pandas.DataFrame()

            data = {'de_logicengine_facts': all_facts}
            t = time.time()
            header = datablock.Header(data_block.taskmanager_id,
                                      create_time=t, creator='logicengine')
            self.data_block_put(data, header, data_block)
        except Exception:  # pragma: no cover
            logging.getLogger().exception("Unexpected error!")
            raise
        else:
            return le_list

    def run_publishers(self, actions, facts, data_block=None):
        """
        Run Publishers in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        if not data_block:
            return
        try:
            for action_list in actions.values():
                for action in action_list:
                    publisher = self.channel.publishers[action]
                    name = publisher.name
                    logging.getLogger().info(f'run publisher {name}')
                    logging.getLogger().debug(f'run publisher {name} {data_block}')
                    publisher.worker.publish(data_block)
        except Exception:
            logging.getLogger().exception("Unexpected error!")
            raise
