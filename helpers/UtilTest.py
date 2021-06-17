import unittest

from constants.index import KikiStore
from utils import add_back_to_pending_list, calculate_total_cost

from helpers.utils import  make_package


class UtilTest(unittest.TestCase):
    def setUp(self):
        KikiStore['base_delivery_cost'] = 100
        main_packages = [
            make_package('PKG1', 50, 30, 'OFR001'),
            make_package('PKG2', 75, 125, 'OFR001'),
            make_package('PKG3', 175, 100, 'OFR001'),
            make_package('PKG4', 110, 60, 'OFR001'),
            make_package('PKG5', 155, 95, 'OFR001'),
        ]
        main_packages.sort()
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


if __name__ == '__main__':
    unittest.main()
