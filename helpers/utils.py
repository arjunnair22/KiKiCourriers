import bisect
from functools import reduce
from constants.index import KikiStore

from Model.Packages import Packages


def less_than(self, other):
    return self.prop < other.prop


def make_package(package_id, package_weight, distance, offer_code):
    return Packages(package_id, package_weight, distance, offer_code)


def find_smallest_package_larger_than(weight, vehicle):
    smallest_package = (None, None, None)
    for index, package in enumerate(vehicle.packages):
        if package.weight >= weight:
            smallest_package = (index, vehicle, package)
            break
    return smallest_package


def get_new_package_list(package, vehicle):
    return vehicle.packages + [package]


def update_package_in_vehicle(data):
    index, vehicle, package = data
    temp = vehicle.packages[index]
    vehicle.packages.append(package)
    return temp, vehicle


def compose(*funcs):
    def composed_function(f, g):
        return lambda x: f(g(x))

    return reduce(composed_function, funcs, lambda x: x)


def add_back_to_pending_list(store):
    def add(package):
        bisect.insort(store["packages"], package)

    return add


def get_smallest_delay(delays):
    pass


def count_greater_than(value):
    def is_greater(iterable):
        return len(iterable) > value

    return is_greater


def is_scheduled_for_delivery(package):
    return not package.scheduled


def schedule(iteration, package):
    # compose function which doesnt require delay calculation
    # compose function which requires delay calculation
    pass


def try_schedule(packages):
    for index, package in enumerate(packages):
        schedule(index + 1, package)


def update_main_store_config(load, speed, vehicle_count):
    return {
        **KikiStore,
        "load": load,
        "speed": speed,
        "vehicle_count": vehicle_count
    }


def will_require_waiting(iteration):
    return iteration > KikiStore.get("vehicle_count")


def can_add_without_replacement(package, schedule_package):
    pass


def add_to_scheduled_packages(package):
    KikiStore["vehicle"]["packages_scheduled"].append(package)


def update_total_weightof_scheduled_packages(package):
    KikiStore["vehicle"]["total_weight"] += package.package_weight


def add_to_scheduled_update_weight(package):
    add_to_scheduled_packages(package)
    update_total_weightof_scheduled_packages(package)


compose(add_back_to_pending_list(KikiStore), update_package_in_vehicle, find_smallest_package_larger_than)


#doesnt require waiting
# check if