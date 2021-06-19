from Model.Packages import Packages
from constants.index import KikiStore, offer_code


def calculate_total_cost(package: Packages):
    delivery_cost = calculate_delivery_cost(package)
    return delivery_cost - calculate_discount(package, delivery_cost)


def find_smallest_package_larger_than(package_info):
    package, weight = package_info
    smallest_package = None, None
    for index, s_package in enumerate(KikiStore.get("vehicle").get("packages_scheduled")):
        if s_package.package_weight >= weight:
            smallest_package = index, package
            break
    return smallest_package


def can_add_without_replacement(package: Packages):
    return package.package_weight <= KikiStore.get("load") - KikiStore.get("vehicle").get("total_weight")


def update_total_weight_of_scheduled_packages(package_weight):
    KikiStore["vehicle"]["total_weight"] += package_weight


def get_weight_difference(package: Packages):
    return package, package.package_weight - (KikiStore.get("load") - KikiStore.get("vehicle").get("total_weight"))


def calculate_discount(package: Packages, delivery_cost):
    try:
        offer = offer_code[package.offer_code]
        if offer.get("weight")[0] <= package.package_weight <= offer.get("weight")[1]:
            if offer.get("distance")[0] <= package.distance <= offer.get("distance")[1]:
                return round(delivery_cost * (offer.get("discount_percent") / 100), 2)
        return 0
    except:
        return 0


def calculate_delivery_cost(package: Packages):
    return round(KikiStore.get("base_delivery_cost") + (package.package_weight * 10) + (package.distance * 5), 2)