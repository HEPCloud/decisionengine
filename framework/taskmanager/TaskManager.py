#!/usr/bin/env python
"""
Task Manager
"""
import threading
import logging
import time
import sys
import uuid
import traceback
import multiprocessing

import decisionengine.framework.dataspace.dataspace as dataspace
import decisionengine.framework.dataspace.datablock as datablock
import decisionengine.framework.configmanager.ConfigManager as configmanager
import decisionengine.framework.modules.de_logger as de_logger

TRANSFORMS_TO = 300

def log_exception(logger, header_message):
    exc, detail, tb = sys.exc_info()
    logger.error("%s %s %s"%(header_message, exc, detail))
    logger.error("Traceback")
    for l in traceback.format_exception(exc, detail, tb):
        logger.error("%s"%(l,))
    logger.error("=======================")
    del tb

class Worker(object):
    """
    Provides interface to loadable modules an events to sycronise
    execution
    """

    def __init__(self, conf_dict):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the worker
        """
        self.worker = configmanager.ConfigManager.create(conf_dict['module'],
                                                         conf_dict['name'],
                                                         conf_dict['parameters'])
        self.module = conf_dict['module']
        self.name = self.worker.__class__.__name__
        self.schedule = conf_dict.get('schedule')
        self.run_counter = 0
        self.data_updated = threading.Event()
        self.stop_running = threading.Event()

class Channel(object):
    """
    Decision Channel.
    Instantiates workers according to channel configuration
    """

    def __init__(self, channel_dict):
        """
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        """

        self.sources = {}
        self.transforms = {}
        self.le_s = {}
        self.publishers = {}
        for s in channel_dict['sources']:
            self.sources[s] = Worker(channel_dict['sources'][s])
        for s in channel_dict['transforms']:
            self.transforms[s] = Worker(channel_dict['transforms'][s])

        for s in channel_dict['logicengines']:
            self.le_s[s] = Worker(channel_dict['logicengines'][s])

        for s in channel_dict['publishers']:
            self.publishers[s] = Worker(channel_dict['publishers'][s])
        self.task_manager = channel_dict.get('task_manager', {})


# states

BOOT, STEADY, OFFLINE, SHUTTINGDOWN, SHUTDOWN = range(5)
_state_names =  ['BOOT', 'STEADY', 'OFFLINE', 'SHUTTINGDOWN', 'SHUTDOWN']

class TaskManager(object):
    """
    Task Manager
    """

    def __init__(self, name, task_manager_id, generation_id, channel_dict, global_config):
        """
        :type task_manager_id: :obj:`int`
        :arg task_manager_id: Task Manager id provided by caller
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        self.dataspace = dataspace.DataSpace(global_config)
        self.data_block_t0 = datablock.DataBlock(self.dataspace,
                                                 name,
                                                 task_manager_id,
                                                 generation_id) # my current data block
        self.name = name
        self.id = task_manager_id
        self.channel = Channel(channel_dict)
        self.state = multiprocessing.Value('i', BOOT)
        self.decision_cycle_active = False
        self.lock = threading.Lock()
        self.logger = de_logger.get_logger()
        self.stop = False # stop running all loops when this is True


    def wait_for_all(self, events_done):
        """
        Wait for all sources or transforms to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """

        self.logger.info("Waiting for all tasks to run")
        while not all([e.isSet() for e in events_done]):
            time.sleep(1)
            if self.stop:
                break
            """
            ev_wait = [e.wait(1) for e in events_done])
            if all(ev_wait):

            evs = [e.is_set() for e in events_done]
            if all(evs):
                break
            """
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

        self.logger.info("Starting Task Manager %s"%(self.id,))
        done_events = self.start_sources(self.data_block_t0)
        # This is a boot phase
        # Wait until all sources run at least one time
        self.wait_for_all(done_events)
        self.logger.info("All sources finished")
        if self.get_state() != BOOT:
            self.logger.error("Error occured during initial run of sources. Task Manager %s exits"%(self.name,))
            sys.exit(1)
        else:
            self.decision_cycle()
        if self.get_state() == BOOT:
            self.set_state(STEADY)
        else:
            self.logger.error("Error occured. Task Manager %s exits"%(self.name,))
            sys.exit(1)

        while self.get_state() == STEADY:
            try:
                self.wait_for_any(done_events)
                self.decision_cycle()
                if self.stop:
                    self.logger.info("Task Manager %s received stop signal and exits"%(self.id,))
                    for s in self.channel.sources:
                        self.channel.sources[s].stop_running.set()
                        time.sleep(5)
                    for t in self.channel.transforms:
                        self.channel.transforms[t].stop_running.set()
                        time.sleep(5)
                    break
            except:
                exc, detail, tb = sys.exc_info()
                self.logger.error("Exception in the task manager main loop %s %s %s"%(exc, detail, traceback.format_exception(exc, detail, tb)))
                break

            time.sleep(1)
        self.logger.error("Error occured. Task Manager %s exits with state %s"%(self.id, _state_names[self.get_state()]))


    def set_state(self, state):
        with self.state.get_lock():
           self.state.value = state

    def get_state(self):
        with self.state.get_lock():
            return self.state.value

    def stop_task_manager(self):
        """
        signal task manager to stop
        """
        self.stop = True

    def offline_task_manager(self, current_data_block):
        """
        offline and stop task manager
        """

        self.set_state(OFFLINE)
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
            self.logger.error('data_block put expecting %s type, got %s'%
                              (dict, type(data)))
            return
        self.logger.debug('data_block_put %s'%(data,))
        with data_block.lock:
            for k in data:
                metadata = datablock.Metadata(data_block.taskmanager_id, generation_id=data_block.generation_id)
                metadata.set_state('END_CYCLE')
                data_block.put(k, data[k], header, metadata=metadata)

    def do_backup(self):
        """
        Duplicate current data block and return its copy

        :rtype: :obj:`~datablock.DataBlock`

        """

        with self.lock:
            data_block = self.data_block_t0.duplicate()
            self.logger.debug('Duplicated block %s'%(data_block,))
        return data_block

    def decision_cycle(self):
        """
        Decision cycle to be run periodically (by trigger)
        """

        data_block_t1 = self.do_backup()
        try:
            self.run_transforms(data_block_t1)
        except Exception:
            log_exception(self.logger, "error in decision cycle(transforms)")
        try:
            actions_facts = self.run_logic_engine(data_block_t1)
            self.logger.info("logic engine returned %s"%(actions_facts,))
            for a_f in actions_facts:
                try:
                    self.run_publishers(a_f['actions'], a_f['newfacts'], data_block_t1)
                except Exception:
                    log_exception(self.logger, "error in decision cycle(publishers)")
        except Exception:
            log_exception(self.logger, "error in decision cycle(logic engine)")

    def run_source(self, src):
        """
        Get the data from source
        and put it into the data block

        :type src: :obj:`~Worker`
        :arg src: source Worker
        """

        while 1:
            try:
                self.logger.info('Src %s calling acquire'%(src.name,))
                data = src.worker.acquire()
                #self.logger.info('Src %s acquire retuned %s'%(src.name, data))
                self.logger.info('Src %s acquire retuned'%(src.name,))
                self.logger.info('Src %s filling header'%(src.name,))
                if data:
                    t = time.time()
                    header = datablock.Header(self.data_block_t0.taskmanager_id,
                                              create_time=t, creator=src.module)
                    self.logger.info('Src %s header done'%(src.name,))
                    self.data_block_put(data, header, self.data_block_t0)
                    self.logger.info('Src %s data block put done'%(src.name,))
                else:
                    self.logger.warning('Src %s acquire retuned no data'%(src.name,))
                src.run_counter += 1
                src.data_updated.set()
                self.logger.info('Src %s %s finished cycle'%(src.name, src.module))
            except Exception:
                exc, detail = sys.exc_info()[:2]
                self.logger.error("error running source %s %s %s" % (src.name, exc, detail))
                self.offline_task_manager(self.data_block_t0)
            s = src.stop_running.wait(src.schedule)
            if s:
                self.logger.info("received stop_running signal for %s"%(src.name,))
                break
        self.logger.info("stopped %s" % (src.name,))

    def start_sources(self, data_block=None):
        """
        Start sources, each in a separate thread

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """

        event_list = []
        for s in self.channel.sources:
            self.logger.info("starting loop for %s" % (s,))
            event_list.append(self.channel.sources[s].data_updated)
            thread = threading.Thread(group=None, target=self.run_source,
                                      name=self.channel.sources[s].name, args=([self.channel.sources[s]]), kwargs={})
            try:
                thread.start()
            except:
                exc, detail = sys.exc_info()[:2]
                self.logger.error("error starting thread %s: %s" % (self.channel.sources[s].name, detail))
                self.offline_task_manager(data_block)
                break
        return event_list

    def run_transforms(self, data_block=None):
        """
        Run transforms.
        So far in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        self.logger.info('run_transforms')
        self.logger.debug('run_transforms: data block %s'%(data_block,))
        if not data_block:
            return
        event_list = []
        for name, transform in self.channel.transforms.items():
            self.logger.info('starting transform %s'%(transform.name,))
            event_list.append(transform.data_updated)
            thread = threading.Thread(group=None,
                                      target=self.run_transform,
                                      name=transform.name,
                                      args=(transform, data_block),
                                      kwargs={})

            try:
                thread.start()
            except:
                exc, detail = sys.exc_info()[:2]
                self.logger.error("error starting thread %s: %s" % (self.channel.transform.name, detail))
                self.offline_task_manager(data_block)
                break

        self.wait_for_all(event_list)
        self.logger.info("all transforms finished")

    def run_transform(self, transform, data_block):
        """
        Run a transform

        :type transform: :obj:`~Worker`
        :arg transform: source Worker
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        data_to = self.channel.task_manager.get('data_TO', TRANSFORMS_TO)
        consume_keys = transform.worker.consumes()

        self.logger.info('transform: %s expected keys: %s provided keys: %s'%(transform.name, consume_keys, data_block.keys()))
        loop_counter = 0
        while 1:
            # Check if data is ready
            if set(consume_keys) <= set(data_block.keys()):
                # data is ready -  may run transform()
                self.logger.info('run transform %s'%(transform.name,))
                try:
                    with data_block.lock:
                        data = transform.worker.transform(data_block)
                    self.logger.debug('transform returned %s'%(data,))
                    t = time.time()
                    header = datablock.Header(data_block.taskmanager_id,
                                              create_time=t,
                                              creator=transform.name)
                    self.data_block_put(data, header, data_block)
                    self.logger.info('transform put data')
                except Exception, detail:
                    self.logger.error('exception from %s: %s'%(transform.name, detail))
                    self.offline_task_manager(data_block)
                break
            else:
                s = transform.stop_running.wait(1)
                if s:
                    self.logger.info("received stop_running signal for %s"%(transform.name,))
                    break
                loop_counter += 1
                if loop_counter == data_to:
                    self.logger.info("transform %s did not get consumes data in %s seconds. Exiting"%(transform.name, data_to))
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
            self.logger.info('run logic engine %s'%(self.channel.le_s[le].name,))
            self.logger.debug('run logic engine %s %s'%(self.channel.le_s[le].name, data_block))
            rc = self.channel.le_s[le].worker.evaluate(data_block)
            le_list.append(rc)
            self.logger.info('run logic engine %s done'%(self.channel.le_s[le].name,))
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
                self.logger.info('run publisher %s'%(self.channel.publishers[action].name))
                self.logger.debug('run publisher %s %s'%(self.channel.publishers[action].name, data_block))
                self.channel.publishers[action].worker.publish(data_block)

if __name__ == '__main__':
    import decisionengine.framework.dataspace.dataspace as dataspace
    import os
    import string

    config_manager = configmanager.ConfigManager()
    config_manager.load()
    global_config = config_manager.get_global_config()
    print "GLOBAL CONF", global_config


    try:
        de_logger.set_logging(log_file_name = global_config['logger']['log_file'],
                              max_file_size = global_config['logger']['max_file_size'],
                              max_backup_count = global_config['logger']['max_backup_count'])
    except Exception, e:
        print e
        sys.exit(1)

    my_logger = logging.getLogger("decision_engine")
    my_logger.info("Starting decision engine")

    if len(sys.argv) > 1:
        channel_name = sys.argv[1]
        channel_conf = os.path.join(config_manager.channel_config_dir, channel_name)
        with open(os.path.abspath(channel_conf), "r") as f:
            channels = {}
            channel_name = channel_name.split('.')[0]
            code = "channels[channel_name]=" + string.join(f.readlines(), "")
            exec(code)
    else:
        channels = config_manager.get_channels()

    ds = dataspace.DataSpace(global_config)
    taskmanager_id = str(uuid.uuid4()).upper()
    generation_id = 1

    task_managers = {}
    data_space = {}
    """
    create channels
    """
    for ch in channels:
        task_managers[ch] = TaskManager(ch, taskmanager_id, generation_id, channels[ch], global_config)

    for key, value in task_managers.iteritems():
        p = multiprocessing.Process(target=value.run, args=(), name="Process-%s"%(key,), kwargs={})
        p.start()

    try:
        while True:
            if len(multiprocessing.active_children()) < 1:
                break
            for tm_name, tm in task_managers.iteritems():
                print "TM %s state %s"%(tm_name, _state_names[tm.get_state()])
            time.sleep(10)
    except (SystemExit, KeyboardInterrupt):
        pass
