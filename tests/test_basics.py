from .__fixtures import customers, products, orders, order_items


def test_that_fundamentals_have_not_changed(orders):
    assert "_RelaRow__data" in orders[0].__dict__


def test_get_simple_value(customers, products):
    assert customers[321]["first_name"] == "Pirkko"
    assert customers[321].first_name == "Pirkko"
    assert products["5-6574-2801"]["name"] == "Sunglasses"
    assert products["5-6574-2801"].name == "Sunglasses"


def test_set_simple_value(products):
    products["5-6574-2801"]["price"] = 99.90
    assert products["5-6574-2801"].price == 99.90
    products["5-6574-2801"].price = 10.90
    assert products["5-6574-2801"]["price"] == 10.90


def test_get_via_reference(order_items):
    assert order_items[0].order.customer.first_name == "Jaakko"
    assert order_items[3].product.name == "Glock 17"
    assert order_items[3]["product"]["vat"] == "15%"


def test_set_via_reference(order_items):
    order_items[3]["product"]["vat"] = "10%"
    assert order_items[3].product.vat == "10%"
    order_items[3].product.vat = "25%"
    assert order_items[3]["product"]["vat"] == "25%"


def test_row_iteration(customers):
    full_names = []
    for customer in customers:
        full_names.append(f"{customer.first_name} {customer.last_name}")
    assert full_names == [
        "Jaakko Jaakkolainen",
        "Pirkko Jaakkolainen",
        "Jack Bauer",
    ]
