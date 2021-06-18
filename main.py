# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import itertools

from helpers.utils import count_greater_than, is_scheduled_for_delivery, try_schedule, \
    print_output_for_scheduled_packages, reset_scheduled_packages


def schedule_delivery(packages):
    count_greater_than_zero = count_greater_than(0)
    while True:
        iteration = 1
        unscheduled_packages = filter(is_scheduled_for_delivery, packages)
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

    pass


