import yaml
import pytest
from pathlib import Path
from relatable import RelaTable

with open(
    Path(__file__).parent.joinpath("resources").joinpath("orders.yaml"), "r"
) as resource_file:
    resources = yaml.safe_load(resource_file)

__customers = RelaTable(primary_key_column="id")
__products = RelaTable(primary_key_column="code")
__orders = RelaTable(foreign_keys={"customer": __customers})
__order_items = RelaTable(foreign_keys={"order": __orders, "product": __products})


@pytest.fixture
def customers():
    global __customers
    __customers.clear()
    for customer in resources["customers"]:
        __customers.append(customer)
    return __customers


@pytest.fixture
def products():
    global __products
    __products.clear()
    for product in resources["products"]:
        __products.append(product)
    return __products


@pytest.fixture
def orders():
    global __orders
    __orders.clear()
    for order in resources["orders"]:
        __orders.append(order)
    return __orders


@pytest.fixture
def order_items():
    global __order_items
    __order_items.clear()
    for order_item in resources["order_items"]:
        __order_items.append(order_item)
    return __order_items
