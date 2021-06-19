

from constants.index import KikiStore
from helpers.utils import count_greater_than, make_package, \
    update_main_store_config
from Scheduler import reset_scheduled_packages, try_schedule, is_scheduled_for_delivery, save_for_delivery, \
    print_output_for_scheduled_packages


def schedule_delivery():
    packages = KikiStore.get("packages")
    count_greater_than_zero = count_greater_than(0)
    while True:
        iteration = 1
        unscheduled_packages = list(filter(is_scheduled_for_delivery, packages))
        if count_greater_than_zero(unscheduled_packages):
            try_schedule(unscheduled_packages)
            print_output_for_scheduled_packages(iteration)
            reset_scheduled_packages()
            iteration += 1
        else:
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # get list of packages and arrange in sorted order
    # schedule delivery of packages
    base_delivery_cost, no_of_packages = input().split(' ')
    KikiStore["base_delivery_cost"] = int(base_delivery_cost)
    packages = []
    for index in range(int(no_of_packages)):
        package_id, weight, distance, offer_code = input().split(' ')
        packages.append((package_id, weight, distance, offer_code))
    no_of_vehicles, max_speed, max_weight = input().split(' ')
    update_main_store_config(int(max_weight), int(max_speed), int(no_of_vehicles))
    for package_id, weight, distance, offer_code in packages:
        save_for_delivery(make_package(package_id, int(weight), int(distance), offer_code))
    schedule_delivery()


