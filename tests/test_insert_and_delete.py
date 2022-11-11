import pytest
from .__orders import customers, products, orders, order_items


def test_simple_append(customers, products, orders, order_items):
    customer = customers.find_first(
        lambda c: c.first_name == "Pirkko" and c.last_name == "Jaakkolainen"
    )
    order = orders.find_first(lambda o: o.customer == customer)
    product = products.find_first(lambda p: p.name == "Bubble gum")

    order_items.append(
        {
            "order": order.primary_key(),
            "product": product.primary_key(),
            "amount": 10,
        }
    )

    item_names = []
    for item in order_items.find(lambda oi: oi.order == order):
        item_names.append(item.product.name)
    assert item_names == [
        "Knockout powder",
        "Purse with a hidden compartment",
        "Bubble gum",
    ]


def test_simple_delete(order_items):
    del order_items[len(order_items) - 1]
    item_names = []
    for item in order_items:
        item_names.append(item.product.name)
    assert item_names == [
        "Sunglasses",
        "Knockout powder",
        "Purse with a hidden compartment",
        "Glock 17",
    ]


def test_insert(products):
    products.insert(
        1,
        {
            "name": "Shoe phone",
            "code": "X-6524-3454",
            "price": None,
            "vat": None,
        },
    )

    product_names = []
    for product in products:
        product_names.append(product.name)

    assert product_names == [
        "Sunglasses",
        "Shoe phone",
        "Glock 17",
        "Purse with a hidden compartment",
        "Knockout powder",
        "Bubble gum",
    ]


def test_insert_failure(orders, customers):
    customer = customers.find_first(
        lambda c: c.first_name == "Pirkko" and c.last_name == "Jaakkolainen"
    )
    with pytest.raises(IndexError):
        orders.insert(0, {"customer": customer.primary_key()})


def test_delete(customers):
    customer = customers.find_first(
        lambda c: c.first_name == "Pirkko" and c.last_name == "Jaakkolainen"
    )
    del customers[customer.primary_key()]
    customer_names = []
    for customer in customers:
        customer_names.append(f"{customer.first_name} {customer.last_name}")
    assert customer_names == ["Jaakko Jaakkolainen", "Jack Bauer"]


def test_delete_failure(orders, customers):
    with pytest.raises(IndexError):
        del orders[0]
    with pytest.raises(IndexError):
        order = orders[1]
        del orders[order.primary_key()]
