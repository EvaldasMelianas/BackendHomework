import unittest
from copy import deepcopy

from classes.discount_rules import DiscountRules
from classes.shipments import Shipments, DiscountManager
from test_variables import test_rates, test_shipments


class TestDiscountRules(unittest.TestCase):
    def setUp(self):
        self.shipments = Shipments(deepcopy(test_shipments), test_rates)
        self.shipments.check_format()
        self.discount_manager = DiscountManager(10)
        self.discount_rules = DiscountRules(self.shipments, self.discount_manager)
        self.discount_rules.apply_rules()

    def test_apply_lp_free_rule(self):
        shipments = self.shipments.get_shipments()
        self.assertEqual(["2015-02-09", "L", "LP", 0.0, 6.9], shipments[8])
        self.assertEqual(["2015-02-11", "L", "LP", 6.9], shipments[12])

    def test_apply_lowest_price_rule(self):
        shipments = self.shipments.get_shipments()
        self.assertEqual(["2015-02-01", "S", "MR", 1.5, 0.5], shipments[0])
        self.assertEqual(["2015-02-17", "S", "MR", 1.9, 0.1], shipments[17])


if __name__ == "__main__":
    unittest.main()
