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
        if package.package_weight >= weight:
            smallest_package = (index, vehicle, package)
            break
    return smallest_package


def get_new_package_list(package, vehicle):
    return vehicle.packages + [package]


def update_package_in_vehicle(data):
    index, vehicle, package = data
    if index is None or vehicle is None or package is None:
        return None
    temp = vehicle.packages[index]
    vehicle.packages.append(package)
    return temp


def compose(*funcs):
    def composed_function(f, g):
        return lambda x: f(g(x))

    return reduce(composed_function, funcs, lambda x: x)


def add_back_to_pending_list(store):
    def add(package):
        if package is None:
            return None
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


def schedule(package: Packages):
    add_to_scheduled_and_update_weight(package)


def add_waiting_time(time_in_hours):
    try:
        waiting_time = KikiStore.get("vehicle").get("delays")[0]
        return time_in_hours + waiting_time
    except:
        return time_in_hours


def try_schedule(iteration, packages):
    for package in packages:
        schedule(package)
    reduce(find_return_time, KikiStore.get("vehicle").get("packages"), 0)


def find_return_time(accumulator, package: Packages):
    time = calculate_time(package)
    return time if time >= accumulator else accumulator


def calculate_time(package: Packages):
    return round(package.distance / KikiStore.get("speed"), 2)


def update_main_store_config(load, speed, vehicle_count):
    return {
        **KikiStore,
        "load": load,
        "speed": speed,
        "vehicle_count": vehicle_count
    }


def will_require_waiting(iteration):
    return iteration > KikiStore.get("vehicle_count")


def can_add_without_replacement(package: Packages):
    return package.package_weight <= KikiStore.get("load") - KikiStore.get("vehicle").get("total_weight")


def add_to_scheduled_packages(package: Packages):
    KikiStore["vehicle"]["packages_scheduled"].append(package)


def update_total_weight_of_scheduled_packages(package: Packages):
    KikiStore["vehicle"]["total_weight"] += package.package_weight


def get_weight_difference(package: Packages):
    return package.package_weight - (KikiStore.get("load") - KikiStore.get("vehicle").get("packages_scheduled"))


optimize_scheduled_packages = compose(add_back_to_pending_list(KikiStore), update_package_in_vehicle,
                                      find_smallest_package_larger_than, get_weight_difference)


def add_to_scheduled_and_update_weight(package: Packages):
    if can_add_without_replacement(package):
        add_to_scheduled_packages(package)
        update_total_weight_of_scheduled_packages(package)
    else:
        optimize_scheduled_packages(package)
