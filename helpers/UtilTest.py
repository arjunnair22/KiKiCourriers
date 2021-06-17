import unittest

from constants.index import KikiStore
from utils import add_back_to_pending_list, calculate_total_cost, update_main_store_config, \
    add_to_scheduled_and_update_weight

from helpers.utils import  make_package


class UtilTest(unittest.TestCase):
    def setUp(self):
        KikiStore['base_delivery_cost'] = 100
        KikiStore["packages"]: []
        update_main_store_config(200,70,2)
        main_packages = [
            make_package('PKG1', 50, 30, 'OFR001'),
            make_package('PKG2', 70, 125, 'OFR001'),
            make_package('PKG2', 75, 125, 'OFR001'),
            make_package('PKG3', 80, 100, 'OFR001'),
            make_package('PKG4', 85, 60, 'OFR001'),
            make_package('PKG4', 90, 60, 'OFR001'),
            make_package('PKG5', 155, 95, 'OFR001'),
        ]
        self.vehicle = KikiStore.get("vehicle")
        self.vehicle["packages_scheduled"] = []
        self.vehicle["total_weight"] = 0

        self.MainStore = {
            "packages": main_packages
        }

    def test_if_packages_maintain_a_sorted_order(self):
        package = make_package('PKG5', 60, 95, 'OFR001')
        add_back_to_pending_list(self.MainStore)(package)
        self.assertIs(self.MainStore["packages"][1], package)

    def test_if_calculate_total_cost_works(self):
        package = make_package('PKG5', 110, 60, 'OFR002')
        cost = calculate_total_cost(package)
        self.assertEqual(cost, 1395)

    def test_packages_are_scheduled_when_load_limit_is_not_reached(self):
        add_to_scheduled_and_update_weight(self.MainStore["packages"][0])
        add_to_scheduled_and_update_weight(self.MainStore["packages"][1])
        scheduled = self.vehicle.get("packages_scheduled")
        weight = self.vehicle.get("total_weight")
        self.assertEqual(len(scheduled), 2)
        self.assertEqual(weight, self.MainStore["packages"][0].package_weight +
                         self.MainStore["packages"][1].package_weight)

    def test_delivery_optimized_for_maximum_weight(self):
        add_to_scheduled_and_update_weight(self.MainStore["packages"][0])
        add_to_scheduled_and_update_weight(self.MainStore["packages"][2])
        add_to_scheduled_and_update_weight(self.MainStore["packages"][3])
        add_to_scheduled_and_update_weight(self.MainStore["packages"][4])
        scheduled = self.vehicle.get("packages_scheduled")
        weight = self.vehicle.get("total_weight")
        self.assertEqual(len(scheduled), 2)
        self.assertEqual(weight, self.MainStore["packages"][3].package_weight +
                         self.MainStore["packages"][4].package_weight)

    def test_delivery_optimized_for_maximum_count_packages(self):
        add_to_scheduled_and_update_weight(make_package('PKG1', 50, 30, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 50, 30, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 50, 30, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 50, 30, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 100, 30, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 100, 30, 'OFR001'))
        scheduled = self.vehicle.get("packages_scheduled")
        weight = self.vehicle.get("total_weight")
        self.assertEqual(len(scheduled), 4)
        self.assertEqual(weight, 200)

    def test_delivery_optimized_for_early_delivery(self):
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 10, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 30, 'OFR001'))
        scheduled:list = self.vehicle.get("packages_scheduled")
        weight = self.vehicle.get("total_weight")
        self.assertEqual(len(scheduled), 1)
        self.assertEqual(weight, 150)
        self.assertEqual(scheduled[0].distance, 10)



if __name__ == '__main__':
    unittest.main()
