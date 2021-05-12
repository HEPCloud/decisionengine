'''
Ensure no circularities in produces and consumes.
'''

import toposort
from collections import OrderedDict

def _produced_products(*worker_lists):
    result = {}
    missing_produces = []
    for worker_list in worker_lists:
        for name, worker in worker_list.items():
            produces = worker.worker._produces.keys()
            if not produces:
                missing_produces.append(name)
            else:
                result.update(dict.fromkeys(produces, name))
    return result, missing_produces

def _consumed_products(*worker_lists):
    result = {}
    missing_consumes = []
    for worker_list in worker_lists:
        for name, worker in worker_list.items():
            consumes = worker.worker._consumes.keys()
            if not consumes:
                missing_consumes.append(name)
            else:
                result[name] = set(consumes)
    return result, missing_consumes

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
            err_msg += ' - ' + module + '\n'
    if missing_consumes:
        err_msg += "\nThe following modules are missing '@consumes' declarations:\n\n"
        for module in missing_consumes:
            err_msg += ' - ' + module + '\n'
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
    sorted_modules = None
    try:
        sorted_modules = set(toposort.toposort_flatten(graph))  # Flatten will trigger any circularity errors
    except Exception as e:
        raise RuntimeError(f"A produces/consumes circularity exists in the configuration:\n{e}")

    sorted_transform_names = sorted_modules.intersection(transforms.keys())
    return OrderedDict([(name, transforms.get(name)) for name in sorted_transform_names])
