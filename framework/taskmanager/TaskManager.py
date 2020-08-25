"""
Task Manager
"""
import enum
import threading
import logging
import time
import sys
import multiprocessing
import pandas

from decisionengine.framework.dataspace import dataspace
from decisionengine.framework.dataspace import datablock
from decisionengine.framework.configmanager import ConfigManager

_TRANSFORMS_TO = 300 # 5 minutes
_DEFAULT_SCHEDULE = 300 # ""


class Worker():
    """
    Provides interface to loadable modules an events to sycronise
    execution
    """

    def __init__(self, conf_dict):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the worker
        """
        self.worker = ConfigManager.ConfigManager.create(conf_dict['module'],
                                                         conf_dict['name'],
                                                         conf_dict['parameters'])
        self.module = conf_dict['module']
        self.name = self.worker.__class__.__name__
        self.schedule = conf_dict.get('schedule', _DEFAULT_SCHEDULE)
        self.run_counter = 0
        self.data_updated = threading.Event()
        self.stop_running = threading.Event()

def _make_workers_for(configs):
    return {name: Worker(e) for name, e in configs.items()}

class Channel():
    """
    Decision Channel.
    Instantiates workers according to channel configuration
    """

    def __init__(self, channel_dict):
        """
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        """

        self.sources = _make_workers_for(channel_dict['sources'])
        self.transforms = _make_workers_for(channel_dict['transforms'])
        self.le_s = _make_workers_for(channel_dict['logicengines'])
        self.publishers = _make_workers_for(channel_dict['publishers'])
        self.task_manager = channel_dict.get('task_manager', {})


class State(enum.Enum):
    BOOT = 0
    STEADY = 1
    OFFLINE = 2
    SHUTTINGDOWN = 3
    SHUTDOWN = 4

class TaskManager():
    """
    Task Manager
    """

    def __init__(self, name, task_manager_id, generation_id, channel_dict, global_config):
        """
        :type task_manager_id: :obj:`int`
        :arg task_manager_id: Task Manager id provided by caller
        :type generation_id: :obj:`int`
        :arg generation_id: Task Manager generation id provided by caller
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        :type global_config: :obj:`dict`
        :arg global_config: global configuration
         """
        self.dataspace = dataspace.DataSpace(global_config)
        self.data_block_t0 = datablock.DataBlock(self.dataspace,
                                                 name,
                                                 task_manager_id,
                                                 generation_id)  # my current data block
        self.name = name
        self.id = task_manager_id
        self.channel = Channel(channel_dict)
        self.state = multiprocessing.Value('i', State.BOOT.value)
        self.loglevel = multiprocessing.Value('i', logging.WARNING)
        self.decision_cycle_active = False
        self.lock = threading.Lock()
        self.stop = False  # stop running all loops when this is True

    def wait_for_all(self, events_done):
        """
        Wait for all sources or transforms to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        logging.info('Waiting for all tasks to run')
        while not all([e.isSet() for e in events_done]):
            time.sleep(1)
            if self.stop:
                break

        for e in events_done:
            e.clear()

    def wait_for_any(self, events_done):
        """
        Wait for any sources to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        while not any([e.isSet() for e in events_done]):
            time.sleep(1)
            if self.stop:
                break

        for e in events_done:
            if e.isSet():
                e.clear()

    def run(self):
        """
        Task Manager main loop
        """
        logging.setLevel(self.loglevel.value)
        logging.info(f'Starting Task Manager {self.id}')
        done_events = self.start_sources(self.data_block_t0)
        # This is a boot phase
        # Wait until all sources run at least one time
        self.wait_for_all(done_events)
        logging.info('All sources finished')
        if self.get_state() != State.BOOT:
            logging.error(
                f'Error occured during initial run of sources. Task Manager {self.name} exits')
            sys.exit(1)

        self.decision_cycle()
        self.set_state(State.STEADY)

        while self.get_state() == State.STEADY:
            try:
                logging.setLevel(self.loglevel.value)
                self.wait_for_any(done_events)
                self.decision_cycle()
                if self.stop:
                    logging.info(f'Task Manager {self.id} received stop signal and exits')
                    for source in self.channel.sources.values():
                        source.stop_running.set()
                        time.sleep(5)
                    for transform in self.channel.transforms:
                        transform.stop_running.set()
                        time.sleep(5)
                    break
            except Exception as e:
                logging.exception(f'Exception in the task manager main loop {e}')
                break
            time.sleep(1)

        # FIXME: Shouldn't the following message be logged only if the
        #        'break' in the exception handler above is reached?
        logging.error('Error occured. Task Manager %s exits with state %s',
                      self.id, self.get_state_name())

    def set_state(self, state):
        with self.state.get_lock():
            self.state.value = state

    def get_state(self):
        with self.state.get_lock():
            return self.state.value

    def get_state_name(self):
        return State(self.get_state()).name

    def set_loglevel(self, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        with self.loglevel.get_lock():
            # Convert from string to int form using technique
            # suggested by logging module
            self.loglevel.value = getattr(logging, log_level)

    def get_loglevel(self):
        with self.loglevel.get_lock():
            return self.loglevel.value

    def _take_offline(self, current_data_block):
        """
        offline and stop task manager
        """

        self.set_state(State.OFFLINE)
        # invalidate data block
        # not implemented yet
        self.stop = True

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
            logging.error(f'data_block put expecting {dict} type, got {type(data)}')
            return
        logging.debug(f'data_block_put {data}')
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
            logging.debug(f'Duplicated block {data_block}')
        return data_block

    def decision_cycle(self):
        """
        Decision cycle to be run periodically (by trigger)
        """

        data_block_t1 = self.do_backup()
        try:
            self.run_transforms(data_block_t1)
        except Exception:
            logging.exception('error in decision cycle(transforms) ')

        actions_facts = []
        try:
            actions_facts = self.run_logic_engine(data_block_t1)
            logging.info('ran all logic engines')
        except Exception as e:
            logging.exception(f'error in decision cycle(logic engine) {e}')

        for a_f in actions_facts:
            try:
                self.run_publishers(
                    a_f['actions'], a_f['newfacts'], data_block_t1)
            except Exception as e:
                logging.exception(f'error in decision cycle(publishers) {e}')

    def run_source(self, src):
        """
        Get the data from source
        and put it into the data block

        :type src: :obj:`~Worker`
        :arg src: source Worker
        """

        while True:
            try:
                logging.info(f'Src {src.name} calling acquire')
                data = src.worker.acquire()
                logging.info(f'Src {src.name} acquire retuned')
                logging.info(f'Src {src.name} filling header')
                if data:
                    t = time.time()
                    header = datablock.Header(self.data_block_t0.taskmanager_id,
                                              create_time=t, creator=src.module)
                    logging.info(f'Src {src.name} header done')
                    self.data_block_put(data, header, self.data_block_t0)
                    logging.info(f'Src {src.name} data block put done')
                else:
                    logging.warning(f'Src {src.name} acquire retuned no data')
                src.run_counter += 1
                src.data_updated.set()
                logging.info(f'Src {src.name} {src.module} finished cycle')
            except Exception as e:
                logging.exception(f'Exception running source {src.name} : {e}')
                self._take_offline(self.data_block_t0)
            if src.schedule > 0:
                s = src.stop_running.wait(src.schedule)
                if s:
                    logging.info(f'received stop_running signal for {src.name}')
                    break
            else:
                logging.info(f'source {src.name} runs only once')
                break
        logging.info(f'stopped {src.name}')

    def start_sources(self, data_block=None):
        """
        Start sources, each in a separate thread

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """

        event_list = []
        for key, source in self.channel.sources.items():
            logging.info(f'starting loop for {key}')
            event_list.append(source.data_updated)
            thread = threading.Thread(target=self.run_source,
                                      name=source.name,
                                      args=(source))
            # Cannot catch exception from function called in separate thread
            thread.start()
        return event_list

    def run_transforms(self, data_block=None):
        """
        Run transforms.
        So far in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        logging.info('run_transforms')
        logging.debug(f'run_transforms: data block {data_block}')
        if not data_block:
            return
        event_list = []
        for key, transform in self.channel.transforms.items():
            logging.info(f'starting transform {key}')
            event_list.append(transform.data_updated)
            thread = threading.Thread(target=self.run_transform,
                                      name=transform.name,
                                      args=(transform, data_block))
            # Cannot catch exception from function called in separate thread
            thread.start()

        self.wait_for_all(event_list)
        logging.info('all transforms finished')

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

        logging.info('transform: %s expected keys: %s provided keys: %s',
                     transform.name, consume_keys, list(data_block.keys()))
        loop_counter = 0
        while True:
            # Check if data is ready
            if set(consume_keys) <= set(data_block.keys()):
                # data is ready -  may run transform()
                logging.info('run transform %s', transform.name)
                try:
                    with data_block.lock:
                        data = transform.worker.transform(data_block)
                    logging.debug(f'transform returned {data}')
                    t = time.time()
                    header = datablock.Header(data_block.taskmanager_id,
                                              create_time=t,
                                              creator=transform.name)
                    self.data_block_put(data, header, data_block)
                    logging.info('transform put data')
                except Exception as e:
                    logging.exception(f'exception from transform {transform.name} : {e}')
                    self._take_offline(data_block)
                break
            s = transform.stop_running.wait(1)
            if s:
                logging.info(f'received stop_running signal for {transform.name}')
                break
            loop_counter += 1
            if loop_counter == data_to:
                logging.info(f'transform {transform.name} did not get consumes data'
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
        for le in self.channel.le_s:
            logging.info('run logic engine %s',
                         self.channel.le_s[le].name)
            logging.debug('run logic engine %s %s',
                          self.channel.le_s[le].name, data_block)
            rc = self.channel.le_s[le].worker.evaluate(data_block)
            le_list.append(rc)
            logging.info('run logic engine %s done',
                         self.channel.le_s[le].name)
            logging.info('logic engine %s generated newfacts: %s',
                         self.channel.le_s[le].name, rc['newfacts'].to_dict(orient='records'))
            logging.info('logic engine %s generated actions: %s',
                         self.channel.le_s[le].name, rc['actions'])

        # Add new facts to the datablock
        # Add empty dataframe if nothing is available
        if le_list:
            all_facts = pandas.concat([i['newfacts']
                                       for i in le_list], ignore_index=True)
        else:
            logging.info('Logic engine(s) did not return any new facts')
            all_facts = pandas.DataFrame()
        data = {'de_logicengine_facts': all_facts}
        t = time.time()
        header = datablock.Header(data_block.taskmanager_id,
                                  create_time=t, creator='logicengine')
        self.data_block_put(data, header, data_block)

        return le_list

    def run_publishers(self, actions, facts, data_block=None):
        """
        Run Publishers in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        if not data_block:
            return
        for key, action_list in actions.items():
            for action in action_list:
                publisher = self.channel.publishers[action]
                name = publisher.name
                logging.info(f'run publisher {name}')
                logging.debug(f'run publisher {name} {data_block}')
                publisher.worker.publish(data_block)
