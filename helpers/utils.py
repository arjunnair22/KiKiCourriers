from functools import reduce
from constants.index import KikiStore


def compose(*funcs):
    def composed_function(f, g):
        return lambda x: f(g(x))

    return reduce(composed_function, funcs, lambda x: x)


def count_greater_than(value):
    def is_greater(iterable):
        return len(iterable) > value

    return is_greater


def update_main_store_config(load, speed, vehicle_count):
    KikiStore["load"] = load
    KikiStore["speed"] = speed
    KikiStore["vehicle_count"] = vehicle_count


