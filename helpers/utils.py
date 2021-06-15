def sort(package_list: list):
    def package_list_key(package):
        return package.weight
    return sorted(package_list, key=package_list_key)


def make_vehicle(vehicle_id, max_speed, max_carriable_weight):
    return {
        "vehicle_id": vehicle_id,
        "max_speed": max_speed,
        "max_carriable_weight": max_carriable_weight
    }


def make_package(package_weight, package_id, distance, offer_code):
    return {
        "package_weight": package_weight,
        "package_id": package_id,
        "distance_in_km":distance,
        "offer_code":offer_code
    }