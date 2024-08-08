import unittest

from test_variables import test_rates
from classes.shipments import Shipments, DiscountManager


class TestShipments(unittest.TestCase):
    def setUp(self):
        self.sample_shipments = [
            ["2015-02-01", "S", "MR"],
            ["2015-02-24", "M", "LP"],
            ["2015-02-29", "CUSPS"],
            ["2015-13-01", "L", "LP"],
            ["2015-02-24", "X", "LP"],
            ["2015-02-24", "S", "XYZ"],
        ]
        self.shipments = Shipments(self.sample_shipments, test_rates)

    def test_check_format(self):
        self.shipments.check_format()
        expected_results = [
            ["2015-02-01", "S", "MR", 2.0],
            ["2015-02-24", "M", "LP", 4.9],
            ["2015-02-29", "CUSPS", "Ignored"],
            ["2015-13-01", "L", "LP", "Ignored"],
            ["2015-02-24", "X", "LP", "Ignored"],
            ["2015-02-24", "S", "XYZ", "Ignored"],
        ]
        self.assertEqual(self.shipments.get_shipments(), expected_results)

    def test_add_discount(self):
        self.shipments.check_format()
        self.shipments.add_discount(0, 1.0)
        self.assertEqual(
            self.shipments.get_shipments()[0], ["2015-02-01", "S", "MR", 1.0, 1.0]
        )
        self.shipments.add_discount(1, 0.0)
        self.assertEqual(
            self.shipments.get_shipments()[1], ["2015-02-24", "M", "LP", 4.9, "-"]
        )


class TestDiscountManager(unittest.TestCase):
    def setUp(self):
        self.manager = DiscountManager()

    def test_initialize_month_key(self):
        month_key = (2015, 2)
        self.manager.initialize_month_key(month_key)
        self.assertEqual(self.manager.discount_fund[month_key], 0.0)

    def test_get_available_discount(self):
        month_key = (2015, 2)
        self.manager.initialize_month_key(month_key)
        self.assertEqual(self.manager.get_available_discount(month_key, 5.0), 5.0)
        self.manager.apply_discount(month_key, 5.0)
        self.assertEqual(self.manager.get_available_discount(month_key, 6.0), 5.0)

    def test_apply_discount(self):
        month_key = (2015, 2)
        self.manager.initialize_month_key(month_key)
        self.manager.apply_discount(month_key, 3.0)
        self.assertEqual(self.manager.discount_fund[month_key], 3.0)


if __name__ == "__main__":
    unittest.main()
