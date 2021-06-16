import unittest

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

        self.MainStore = {
            "packages": main_packages
        }

        self.vehicles = []
        for index in range(2):
            self.vehicles.append(make_vehicle(index, 70, 200))

    def test_sort

if __name__ == '__main__':
    unittest.main()
