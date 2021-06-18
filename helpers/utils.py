import bisect
from functools import reduce
from constants.index import KikiStore, offer_code

from Model.Packages import Packages


def make_package(package_id, package_weight, distance, package_offer_code):
    return Packages(package_id, package_weight, distance, package_offer_code)


def find_smallest_package_larger_than(package_info):
    package, weight = package_info
    smallest_package = None, None
    for index, s_package in enumerate(KikiStore.get("vehicle").get("packages_scheduled")):
        if s_package.package_weight >= weight:
            smallest_package = index, package
            break
    return smallest_package


def get_new_package_list(package, vehicle):
    return vehicle.packages + [package]


def condition_for_replacing_package(replacement_candidate: Packages, new_package: Packages):
    return replacement_candidate.distance > new_package.distance


def is_same_weight_package(replacement_candidate: Packages, new_package: Packages):
    return replacement_candidate.package_weight == new_package.package_weight


def update_package_in_vehicle(data):
    index, package = data
    if index is None or package is None:
        return None
    scheduled_packages = KikiStore.get("vehicle").get("packages_scheduled")
    replacement_candidate: Packages = scheduled_packages[index]

    if not is_same_weight_package(replacement_candidate, package) or \
            condition_for_replacing_package(replacement_candidate, package):
        return update_and_return_replaced_package(index, package, scheduled_packages)

    return None


def update_and_return_replaced_package(index, package: Packages, scheduled_packages):
    temp: Packages = scheduled_packages.pop(index)
    add_to_scheduled_packages(package)

    update_total_weight_of_scheduled_packages(package.package_weight - temp.package_weight)
    return temp


def compose(*funcs):
    def composed_function(f, g):
        return lambda x: f(g(x))

    return reduce(composed_function, funcs, lambda x: x)


def add_back_to_pending_list(store):
    def add(package: Packages):
        if package is None:
            return None
        bisect.insort(store["packages"], package)
        package.is_scheduled = False
        return True

    return add


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
        waiting_time = KikiStore.get("vehicle").get("delays").pop(0)
        bisect.insort(KikiStore.get("vehicle").get("delays"), time_in_hours + waiting_time)
        return time_in_hours + waiting_time
    except:
        return time_in_hours


def try_schedule(packages):
    for package in packages:
        schedule(package)
    calculate_waiting_period_of_scheduled_vehicle()


def calculate_waiting_period_of_scheduled_vehicle():
    max_time = reduce(find_max_return_time_of_vehicle, KikiStore.get("vehicle").get("packages_scheduled"))
    bisect.insort(KikiStore.get("vehicle").get("delays"), max_time)


def print_output_for_scheduled_packages(iteration):
    for package in KikiStore.get("vehicle").get("packages_scheduled"):
        time_in_hours = (
            calculate_time if will_require_waiting(iteration) else compose(add_waiting_time, calculate_time))(package)
        print(package.package_id, calculate_discount(package, calculate_delivery_cost(package)),
              calculate_total_cost(package), time_in_hours)


def find_max_return_time_of_vehicle(pkg1: Packages, pkg2: Packages):
    return max(calculate_time(pkg2), calculate_time(pkg1))


def calculate_time(package: Packages):
    return round(package.distance / KikiStore.get("speed"), 2)


def update_main_store_config(load, speed, vehicle_count):
    KikiStore["load"] = load
    KikiStore["speed"] = speed
    KikiStore["vehicle_count"] = vehicle_count


def will_require_waiting(iteration):
    return iteration > KikiStore.get("vehicle_count")


def can_add_without_replacement(package: Packages):
    return package.package_weight <= KikiStore.get("load") - KikiStore.get("vehicle").get("total_weight")


def add_to_scheduled_packages(package: Packages):
    KikiStore["vehicle"]["packages_scheduled"].append(package)
    package.is_scheduled = True


def update_total_weight_of_scheduled_packages(package_weight):
    KikiStore["vehicle"]["total_weight"] += package_weight


def get_weight_difference(package: Packages):
    return package, package.package_weight - (KikiStore.get("load") - KikiStore.get("vehicle").get("total_weight"))


optimize_scheduled_packages = compose(add_back_to_pending_list(KikiStore),
                                      update_package_in_vehicle,
                                      find_smallest_package_larger_than, get_weight_difference)


def add_to_scheduled_and_update_weight(package: Packages):
    if can_add_without_replacement(package):
        add_to_scheduled_packages(package)
        update_total_weight_of_scheduled_packages(package.package_weight)
    else:
        optimize_scheduled_packages(package)


def calculate_discount(package: Packages, delivery_cost):
    try:
        offer = offer_code[package.offer_code]
        if offer.get("weight")[0] <= package.package_weight <= offer.get("weight")[1]:
            if offer.get("distance")[0] <= package.distance <= offer.get("distance")[1]:
                return round(delivery_cost * (offer.get("discount_percent") / 100), 2)
    except:
        return 0


def calculate_delivery_cost(package: Packages):
    return round(KikiStore.get("base_delivery_cost") + (package.package_weight * 10) + (package.distance * 5), 2)


def calculate_total_cost(package: Packages):
    delivery_cost = calculate_delivery_cost(package)
    return delivery_cost - calculate_discount(package, delivery_cost)


def reset_scheduled_packages():
    KikiStore.get("vehicle").get("packages_scheduled").clear()
    KikiStore.get("vehicle")["total_weight"] = 0
