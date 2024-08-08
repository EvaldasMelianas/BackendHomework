class DiscountRules:
    def __init__(self, shipments, discount_manager):
        self.shipments = shipments
        self.manager = discount_manager
        self.rates = shipments.get_rates()
        self.lowest_s_price = min(rates["S"] for rates in self.rates.values())
        self.lp_l_counter = {}

    def apply_lowest_price_rule(self):
        for i, shipment in enumerate(self.shipments.get_shipments()):
            if shipment[1] == "S" and "Ignored" not in shipment:
                discount = shipment[3] - self.lowest_s_price
                available_discount = self.manager.get_available_discount(
                    shipment[0][:7], discount
                )
                self.manager.update_fund(shipment[0][:7], available_discount)
                self.shipments.add_discount(i, available_discount)

    def apply_third_large_lp_free_rule(self):
        for i, shipment in enumerate(self.shipments.get_shipments()):
            if shipment[2] == "LP" and shipment[1] == "L":
                month = shipment[0][:7]
                if month not in self.lp_l_counter:
                    self.lp_l_counter[month] = 0
                self.lp_l_counter[month] += 1
                if self.lp_l_counter[month] == 3:
                    available_discount = self.manager.get_available_discount(
                        shipment[0][:7], shipment[3]
                    )
                    self.manager.update_fund(shipment[0][:7], available_discount)
                    self.shipments.add_discount(i, available_discount)

    def apply_rules(self):
        self.apply_third_large_lp_free_rule()
        self.apply_lowest_price_rule()
