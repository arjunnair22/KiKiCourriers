import unittest

from constants.index import KikiStore
from utils import add_back_to_pending_list, calculate_total_cost, update_main_store_config, \
    add_to_scheduled_and_update_weight, calculate_waiting_period_of_scheduled_vehicle, try_schedule, \
    reset_scheduled_packages

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
        self.pack1 = make_package('PKG1', 50, 30, 'OFR001')
        self.pack2 = make_package('PKG2', 75, 125, 'OFR001')
        self.pack3 = make_package('PKG3', 175, 100, 'OFR001')
        self.pack4 = make_package('PKG4', 110, 60, 'OFR001')
        self.pack5 = make_package('PKG5', 155, 95, 'OFR001')
        self.multiple_iters = [self.pack1, self.pack2, self.pack3, self.pack4, self.pack5]
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
        for p in scheduled:
            self.assertTrue(p.is_scheduled)

    def test_delivery_optimized_for_early_delivery(self):
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 10, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 30, 'OFR001'))
        scheduled:list = self.vehicle.get("packages_scheduled")
        weight = self.vehicle.get("total_weight")
        self.assertEqual(len(scheduled), 1)
        self.assertEqual(weight, 150)
        self.assertEqual(scheduled[0].distance, 10)
        for p in scheduled:
            self.assertTrue(p.is_scheduled)

    def test_whether_vehicle_return_time_calculated_correct(self):
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 10, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 30, 'OFR001'))
        calculate_waiting_period_of_scheduled_vehicle()
        expected_delay = round(10/KikiStore.get("speed"),2)
        self.assertEqual(KikiStore.get("vehicle").get("delays")[0], expected_delay)

    def test_calculated_time_matches_with_multiple_scheduled_packages(self):
        add_to_scheduled_and_update_weight(make_package('PKG1', 150, 10, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 20, 50, 'OFR001'))
        add_to_scheduled_and_update_weight(make_package('PKG1', 20, 30, 'OFR001'))
        calculate_waiting_period_of_scheduled_vehicle()
        expected_delay = round(50/KikiStore.get("speed"),2)
        self.assertEqual(KikiStore.get("vehicle").get("delays")[0], expected_delay)

    def test_scheduling_with_one_package(self):
        pack1 = make_package('PKG1', 150, 10, 'OFR001')
        packages = [pack1]
        try_schedule(packages)
        scheduled = KikiStore.get("vehicle").get("packages_scheduled")
        self.assertEqual(len(scheduled), 1)
        self.assertIs(scheduled[0], pack1)

    def test_scheduling_with_multiple_package(self):
        pack1 = make_package('PKG1', 50, 30, 'OFR001')
        pack2 = make_package('PKG2', 75, 125, 'OFR001')
        pack3 = make_package('PKG3', 175, 100, 'OFR001')
        pack4 = make_package('PKG4', 110, 60, 'OFR001')
        pack5 = make_package('PKG5', 155, 95, 'OFR001')
        packages = sorted([pack1, pack2, pack3, pack4, pack5], key=lambda x: x.package_weight)
        KikiStore["packages"] = packages
        try_schedule(packages)
        scheduled = KikiStore.get("vehicle").get("packages_scheduled")
        self.assertEqual(len(scheduled), 2)
        self.assertIn(pack2, scheduled)
        self.assertIn(pack4, scheduled)

    def test_scheduling_with_multiple_package_multiple_iters(self):
        packages = sorted(self.multiple_iters, key=lambda x: x.package_weight)
        KikiStore["packages"] = packages
        try_schedule(packages)
        scheduled = KikiStore.get("vehicle").get("packages_scheduled")
        self.assertEqual(len(scheduled), 2)
        self.assertIn(self.pack2, scheduled)
        self.assertIn(self.pack4, scheduled)
        reset_scheduled_packages()
        next_packages = sorted([self.pack1, self.pack3, self.pack5], key=lambda x: x.package_weight)
        try_schedule(next_packages)
        self.assertEqual(len(scheduled), 1)
        self.assertIn(self.pack3, scheduled)







if __name__ == '__main__':
    unittest.main()
