from datetime import datetime

from constant.constants import PROVIDER_RATES, MONTHLY_DISCOUNT


class Shipments:
    def __init__(self, shipments, rates=PROVIDER_RATES):
        self.shipments = shipments
        self.rates = rates

    def get_shipments(self):
        return self.shipments

    def get_rates(self):
        return self.rates

    def add_discount(self, index, discount):
        self.shipments[index][3] -= round(discount, 2)
        self.shipments[index].append(round(discount, 2) if discount > 0 else "-")

    def check_format(self):
        for item in self.shipments:
            if len(item) != 3:
                item.append("Ignored")
            else:
                date, size, provider = item
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    item.append("Ignored")
                    continue
                if provider not in self.rates or size not in self.rates[provider]:
                    item.append("Ignored")
                else:
                    item.append(self.rates[provider][size])


class DiscountManager:
    def __init__(self, allowed_sum=MONTHLY_DISCOUNT):
        self.discount_fund = {}
        self.allowed_sum = allowed_sum

    def update_fund(self, month_key, discount):
        self.apply_discount(month_key, discount)

    def initialize_month_key(self, month_key):
        if month_key not in self.discount_fund:
            self.discount_fund[month_key] = 0.0

    def get_available_discount(self, month_key, discount):
        self.initialize_month_key(month_key)
        return min(discount, self.allowed_sum - self.discount_fund[month_key])

    def apply_discount(self, month_key, discount):
        self.discount_fund[month_key] += round(discount, 2)
