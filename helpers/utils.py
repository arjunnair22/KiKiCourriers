import bisect
from functools import reduce

from Model.Packages import Packages


def less_than(self, other):
    return self.prop < other.prop


def sort(package_list: list):
    def package_list_key(package):
        return package.weight

    return sorted(package_list, key=package_list_key)


def make_vehicle(vehicle_id, max_speed, max_carriable_weight):
    return {
        "vehicle_id": vehicle_id,
        "max_speed": max_speed,
        "max_carriable_weight": max_carriable_weight,
        "packages": []
    }


def make_package( package_id, package_weight, distance, offer_code):
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
    return reduce(composed_function, funcs, lambda x:x)


def add_back_to_pending_list(store):
    def add(package):
        bisect.insort(store["packages"], package)
    return add


KikiStore = {"packages": []}

compose(add_back_to_pending_list(KikiStore), update_package_in_vehicle, find_smallest_package_larger_than)