import bisect

from Model.Packages import Packages
from constants.index import KikiStore
from helpers.utils import compose
from Vehicle import find_smallest_package_larger_than, can_add_without_replacement, \
    update_total_weight_of_scheduled_packages, get_weight_difference, calculate_discount, calculate_delivery_cost, \
    calculate_total_cost


def reset_scheduled_packages():
    KikiStore.get("vehicle").get("packages_scheduled").clear()
    KikiStore.get("vehicle")["total_weight"] = 0


def add_to_scheduled_and_update_weight(package: Packages):
    if can_add_without_replacement(package):
        add_to_scheduled_packages(package)
        update_total_weight_of_scheduled_packages(package.package_weight)
    else:
        optimize_scheduled_packages(package)


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


def add_back_to_pending_list(store):
    def add(package: Packages):
        if package is None:
            return None
        package.is_scheduled = False
        return True
    return add


optimize_scheduled_packages = compose(add_back_to_pending_list(KikiStore),
                                      update_package_in_vehicle,
                                      find_smallest_package_larger_than, get_weight_difference)


def add_to_scheduled_packages(package: Packages):
    KikiStore["vehicle"]["packages_scheduled"].append(package)
    package.is_scheduled = True


def try_schedule(packages):
    for package in packages:
        schedule(package)
    calculate_waiting_period_of_scheduled_vehicle()


def schedule(package: Packages):
    add_to_scheduled_and_update_weight(package)


def is_scheduled_for_delivery(package):
    return not package.is_scheduled


def update_and_return_replaced_package(index, package: Packages, scheduled_packages):
    temp: Packages = scheduled_packages.pop(index)
    add_to_scheduled_packages(package)

    update_total_weight_of_scheduled_packages(package.package_weight - temp.package_weight)
    return temp


def save_for_delivery(package: Packages):
    bisect.insort(KikiStore.get("packages"), package)


def get_new_package_list(package, vehicle):
    return vehicle.packages + [package]


def condition_for_replacing_package(replacement_candidate: Packages, new_package: Packages):
    return replacement_candidate.distance > new_package.distance


def is_same_weight_package(replacement_candidate: Packages, new_package: Packages):
    return replacement_candidate.package_weight == new_package.package_weight


def add_waiting_time(time_in_hours):
    try:
        waiting_time = KikiStore.get("vehicle").get("delays").pop(0)
        bisect.insort(KikiStore.get("vehicle").get("delays"), time_in_hours + waiting_time)
        return time_in_hours + waiting_time
    except:
        return time_in_hours


def calculate_waiting_period_of_scheduled_vehicle():
    package = max(KikiStore.get("vehicle").get("packages_scheduled"), key=lambda x: x.time_for_delivery)
    bisect.insort(KikiStore.get("vehicle").get("delays"), package.time_for_delivery)


def print_output_for_scheduled_packages(iteration):
    for package in KikiStore.get("vehicle").get("packages_scheduled"):
        time_in_hours = package.time_for_delivery if will_require_waiting(iteration) \
            else add_waiting_time(package.time_for_delivery)
        print(package.package_id, calculate_discount(package, calculate_delivery_cost(package)),
              calculate_total_cost(package), time_in_hours)


def calculate_time(distance: int):
    return round(distance / KikiStore.get("speed"), 2)


def will_require_waiting(iteration):
    return iteration <= KikiStore.get("vehicle_count")


def make_package(package_id, package_weight, distance, package_offer_code):
    return Packages(package_id, package_weight, distance, package_offer_code, calculate_time(distance))
