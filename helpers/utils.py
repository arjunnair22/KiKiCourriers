def sort(package_list: list):
    def package_list_key(package):
        return package.weight
    return sorted(package_list, key=package_list_key)


def make_vehicle():
    return {
        ""
    }


def make_package(package_weight, package_id):
    return {
        "package_weight": package_weight,
        "package_id": package_id
    }