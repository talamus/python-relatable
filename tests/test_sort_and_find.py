from .__fixtures import customers, products, orders, order_items


def test_sorting_rows(customers, order_items):
    customers.sort(key=lambda c: f"{c.last_name} {c.first_name}")
    full_names = []
    for customer in customers:
        full_names.append(f"{customer.first_name} {customer.last_name}")
    assert full_names == [
        "Jack Bauer",
        "Jaakko Jaakkolainen",
        "Pirkko Jaakkolainen",
    ]
    assert order_items[0].order.customer.first_name == "Jaakko"


def test_finding_rows(customers):
    view = customers.find(lambda c: c.last_name == "Jaakkolainen")
    full_names = []
    for customer in view:
        full_names.append(f"{customer.first_name} {customer.last_name}")
    assert full_names == [
        "Jaakko Jaakkolainen",
        "Pirkko Jaakkolainen",
    ]


def test_finding_first_row(customers):
    customer = customers.find_first(lambda c: c.last_name == "Jaakkolainen")
    assert customer.first_name == "Jaakko"
    assert customer.last_name == "Jaakkolainen"


def test_find_all_items_ordered_by_jack_bauer(customers, orders, order_items):
    customer = customers.find(
        lambda c: c.first_name == "Jack" and c.last_name == "Bauer"
    )
    assert len(customer) == 1
    customer = customer[0]
    order = orders.find(lambda o: o.customer == customer)
    assert len(order) == 1
    order = order[0]
    items = order_items.find(lambda i: i.order == order)
    assert len(items) == 2
    item_names = []
    for item in items:
        item_names.append(item.product.name)
    assert item_names == [
        "Glock 17",
        "Sunglasses",
    ]
