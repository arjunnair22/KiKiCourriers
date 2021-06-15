from functools import reduce

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


def make_package(package_weight, package_id, distance, offer_code):
    return {
        "package_weight": package_weight,
        "package_id": package_id,
        "distance_in_km": distance,
        "offer_code": offer_code
    }


def find_smallest_package_larger_than(weight, package_list):
    smallest_package = (None, None)
    for index, package in enumerate(package_list):
        if package.weight >= weight:
            smallest_package = (index, package)
            break
    return smallest_package


def get_updated_package_for_vehicle(package, vehicle):
    return vehicle.packages + [package]


def update_package_in_vehicle(package, vehicle, index):
    temp = vehicle.packages[index]
    vehicle.packages[index] = package
    return temp


def compose(*funcs):
    def composed_function(f, g):
        return lambda x: f(g(x))
    return reduce(composed_function, funcs, lambda x:x)


compose(get_updated_package_for_vehicle, update_package_in_vehicle,find_smallest_package_larger_than)