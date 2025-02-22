# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Ensure no circularities in produces and consumes.
"""

import importlib

from collections import OrderedDict

import structlog
import toposort

from decisionengine.framework.logicengine.LogicEngine import LogicEngine, passthrough_configuration
from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME
from decisionengine.framework.modules.Publisher import Publisher
from decisionengine.framework.modules.Transform import Transform
from decisionengine.framework.taskmanager.PublisherStatus import PublisherStatus
from decisionengine.framework.util.subclasses import all_subclasses

_DEFAULT_SCHEDULE = 300  # 5 minutes

_DELOGGER = structlog.getLogger(LOGGERNAME)
_DELOGGER = _DELOGGER.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


def _produced_products(*worker_lists):
    result = {}
    missing_produces = []
    for worker_list in worker_lists:
        for name, worker in worker_list.items():
            produces = worker.module_instance._produces.keys()
            if not produces:
                missing_produces.append(name)
            else:
                result.update(dict.fromkeys(produces, name))
    result.update(publisher_status=PublisherStatus.__name__)
    return result, missing_produces


def _consumed_products(*worker_lists):
    result = {}
    missing_consumes = []
    for worker_list in worker_lists:
        for name, worker in worker_list.items():
            consumes = worker.module_instance._consumes.keys()
            if not consumes:
                missing_consumes.append(name)
            else:
                result[name] = set(consumes)
    return result, missing_consumes


def source_products(source_workers):
    expected_source_products = set()
    for worker in source_workers.values():
        # FIXME: Just keeping track of instance names will not
        #        work whenever we have multiple source instances
        #        of the same source type.
        expected_source_products.update(worker.module_instance._produces.keys())
    return expected_source_products


def ensure_no_circularities(sources, transforms, publishers):
    """
    Ensures no circularities among data products.
    """
    produced, missing_produces = _produced_products(sources, transforms)
    consumed, missing_consumes = _consumed_products(transforms, publishers)

    err_msg = ""
    if missing_produces:
        err_msg += "\nThe following modules are missing '@produces' declarations:\n\n"
        for module in missing_produces:
            err_msg += " - " + module + "\n"
    if missing_consumes:
        err_msg += "\nThe following modules are missing '@consumes' declarations:\n\n"
        for module in missing_consumes:
            err_msg += " - " + module + "\n"
    if err_msg:
        raise RuntimeError(err_msg)

    # Check that products to be consumed are actually produced
    all_consumes = set()
    all_consumes.update(*consumed.values())
    all_produces = set(produced.keys())
    if not all_consumes.issubset(all_produces):
        extra_keys = list(all_consumes - all_produces)
        raise RuntimeError(f"The following products are required but not produced:\n{extra_keys}")

    graph = {}
    for consumer, products in consumed.items():
        graph[consumer] = set(map(lambda p: produced.get(p), products))

    # Do the check
    sorted_module_names = None
    try:
        sorted_module_names = toposort.toposort_flatten(graph)  # Flatten will trigger any circularity errors
    except Exception as e:
        raise RuntimeError(f"A produces/consumes circularity exists in the configuration:\n{e}")

    # Keep only transforms
    for name in set(sorted_module_names).difference(transforms.keys()):
        sorted_module_names.remove(name)
    return OrderedDict([(name, transforms.get(name)) for name in sorted_module_names])


def _find_only_one_subclass(module, base_class):
    """
    Search through module looking for only one subclass of the supplied base_class
    """
    subclasses = all_subclasses(module, base_class)
    if not subclasses:
        raise RuntimeError(
            f"Could not find a decision-engine '{base_class.__name__}' in the module '{module.__name__}'"
        )
    if len(subclasses) > 1:
        error_msg = (
            f"Found more than one decision-engine '{base_class.__name__}' in the module '{module.__name__}':\n\n"
        )
        for cls in subclasses:
            error_msg += " - " + cls + "\n"
        error_msg += "\nSpecify which subclass you want via the configuration 'name: <one of the above>'."
        raise RuntimeError(error_msg)
    return subclasses[0]


def _create_module_instance(config_dict, base_class, channel_name):
    """
    Create instance of dynamically loaded module
    """
    my_module = importlib.import_module(config_dict["module"])
    class_name = config_dict.get("name")
    if class_name is None:
        if base_class == LogicEngine:
            # Icky kludge until we remove explicit LogicEngine 'module' specification
            class_name = "LogicEngine"
        else:
            class_name = _find_only_one_subclass(my_module, base_class)

    _DELOGGER.debug(f"in TaskManager, importlib has imported module {class_name}")
    class_type = getattr(my_module, class_name)
    return class_type(dict(**config_dict["parameters"], channel_name=channel_name))


class Worker:
    """
    Provides interface to loadable modules an events to synchronise
    execution
    """

    def __init__(self, key, conf_dict, base_class, channel_name):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the worker
        """
        self.module_instance = _create_module_instance(conf_dict, base_class, channel_name)
        self.module = conf_dict["module"]
        self.module_key = key
        self.name = self.module_instance.__class__.__name__
        self.schedule = conf_dict.get("schedule", _DEFAULT_SCHEDULE)

        # NOTE: THIS MUST BE LOGGED TO de logger, because channel logger does not exist yet
        _DELOGGER.debug(
            f"Creating worker: module={self.module} name={self.module_key} class_name={self.name} parameters={conf_dict['parameters']} schedule={self.schedule}"
        )


def _make_workers_for(configs, base_class, channel_name):
    return {key: Worker(key, e, base_class, channel_name) for key, e in configs.items()}


def channel_workers(channel_name, channel_config, logger):
    logger.debug("Creating channel publishers")
    publisher_workers = _make_workers_for(channel_config["publishers"], Publisher, channel_name)

    logger.debug("Creating channel logic engines")
    configured_le_s = channel_config.get("logicengines")
    if configured_le_s is None:
        logger.debug(
            "No 'logicengines' configuration detected; will use default configuration, which unconditionally executes all configured publishers."
        )
        configured_le_s = passthrough_configuration(channel_config["publishers"].keys())
    if len(configured_le_s) > 1:
        raise RuntimeError("Cannot support more than one logic engine per channel.")

    logic_engine_worker = None
    if configured_le_s:
        key, config = configured_le_s.popitem()
        logic_engine_worker = Worker(key, config, LogicEngine, channel_name)

    logger.debug("Creating channel transforms")
    transform_workers = _make_workers_for(channel_config["transforms"], Transform, channel_name)
    return (transform_workers, logic_engine_worker, publisher_workers)


def validated_workflow(channel_name, sources, channel_config, logger=structlog.getLogger()):
    transforms, logic_engine, publishers = channel_workers(channel_name, channel_config, logger)
    transforms = ensure_no_circularities(sources, transforms, publishers)
    return {
        "sources": sources,
        "transforms": transforms,
        "logic_engine": logic_engine,
        "publishers": publishers,
    }
