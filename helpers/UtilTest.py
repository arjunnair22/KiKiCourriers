import unittest
from utils import add_back_to_pending_list

from helpers.utils import make_vehicle, make_package


class UtilTest(unittest.TestCase):
    def setUp(self):
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

        self.vehicles = []
        for index in range(2):
            self.vehicles.append(make_vehicle(index, 70, 200))

    def test_if_packages_maintain_a_sorted_order(self):
        package = make_package('PKG5', 60, 95, 'OFR001')
        add_back_to_pending_list(self.MainStore)(package)
        self.assertIs(self.MainStore["packages"][1], package)


if __name__ == '__main__':
    unittest.main()
