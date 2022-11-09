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


def test_str_and_repr(order_items):
    assert repr(order_items) == (
        "[{'order': 0, 'product': '5-6574-2801', 'amount': 1}, "
        "{'order': 1, 'product': '8-7635-2345', 'amount': 2}, "
        "{'order': 1, 'product': '1-1864-3541', 'amount': 1}, "
        "{'order': 2, 'product': '9-7624-5276', 'amount': 1}, "
        "{'order': 2, 'product': '5-6574-2801', 'amount': 1}]"
    )
    assert str(order_items) == (
        "["
            "{"
                "'order': {"
                    "'customer': {"
                        "'id': 100, "
                        "'first_name': 'Jaakko', "
                        "'last_name': 'Jaakkolainen', "
                        "'address': 'Kehäkatu 12 A 5\\n15870 Hollola', "
                        "'country': 'Finland'"
                    "}"
                "}, "
                "'product': {"
                    "'name': 'Sunglasses', "
                    "'code': '5-6574-2801', "
                    "'price': 10.9, "
                    "'vat': '20%'"
                "}, "
                "'amount': 1"
            "}, "
            "{"
                "'order': {"
                    "'customer': {"
                        "'id': 321, "
                        "'first_name': 'Pirkko', "
                        "'last_name': 'Jaakkolainen', "
                        "'address': 'Kehäkatu 12 A 5\\n15870 Hollola', "
                        "'country': 'Finland'"
                    "}"
                "}, "
                "'product': {"
                    "'name': 'Knockout powder', "
                    "'code': '8-7635-2345', "
                    "'price': 85.5, "
                    "'vat': '10%'"
                "}, "
                "'amount': 2"
            "}, "
            "{"
                "'order': {"
                    "'customer': {"
                        "'id': 321, "
                        "'first_name': 'Pirkko', "
                        "'last_name': 'Jaakkolainen', "
                        "'address': 'Kehäkatu 12 A 5\\n15870 Hollola', "
                        "'country': 'Finland'"
                    "}"
                "}, "
                "'product': {"
                    "'name': 'Purse with a hidden compartment', "
                    "'code': '1-1864-3541', "
                    "'price': 199.0, "
                    "'vat': '20%'"
                "}, "
                "'amount': 1"
            "}, "
            "{"
                "'order': {"
                    "'customer': {"
                        "'id': 999, "
                        "'first_name': 'Jack', "
                        "'last_name': 'Bauer', "
                        "'address': '935 Pennsylvania Avenue NW\\nWashington, DC 20535', "
                        "'country': 'United States'"
                    "}"
                "}, "
                "'product': {"
                    "'name': 'Glock 17', "
                    "'code': '9-7624-5276', "
                    "'price': 512.99, "
                    "'vat': '25%'"
                "}, "
                "'amount': 1"
            "}, "
            "{"
                "'order': {"
                    "'customer': {"
                        "'id': 999, "
                        "'first_name': 'Jack', "
                        "'last_name': 'Bauer', "
                        "'address': '935 Pennsylvania Avenue NW\\nWashington, DC 20535', "
                        "'country': 'United States'"
                    "}"
                "}, "
                "'product': {"
                    "'name': 'Sunglasses', "
                    "'code': '5-6574-2801', "
                    "'price': 10.9, "
                    "'vat': '20%'"
                "}, "
                "'amount': 1"
            "}"
        "]"
    )
