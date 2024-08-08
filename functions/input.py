from classes.shipments import Shipments, DiscountManager
from classes.discount_rules import DiscountRules


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()
        return [line.strip().split() for line in lines]


def process_shipments(data):
    shipments = Shipments(data)
    shipments.check_format()
    discount_manager = DiscountManager()
    discount_rules = DiscountRules(shipments, discount_manager)
    discount_rules.apply_rules()
    return shipments


def output_shipments():
    data = read_input()
    shipments = process_shipments(data)
    for shipment in shipments.get_shipments():
        if "Ignored" not in shipment and len(shipment) == 4:
            shipment.append("-")
        formatted_shipment = [
            f"{item:.2f}" if isinstance(item, float) else str(item) for item in shipment
        ]
        print(" ".join(formatted_shipment))
