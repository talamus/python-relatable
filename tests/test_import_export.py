import pytest
from relatable import RelaTable


def test_import_and_export_during_init():
    list_of_objects = [
        {"name": "cakes", "amount": 40},
        {"name": "banana", "amount": 59},
        {"name": "knitting needles", "amount": 13},
        {"name": "white out", "amount": 81},
        {"name": "magnet", "amount": 74},
        {"name": "zebra", "amount": -1},
        {"name": "cow", "amount": 209},
        {"name": "trucks", "amount": 99},
        {"name": "envelope", "amount": 100},
        {"name": "pen", "amount": 25},
        {"name": "paperclip", "amount": 500},
    ]
    table = RelaTable(rows=list_of_objects)
    assert table.export() == list_of_objects


def test_import_and_export_via_rows():
    list_of_objects = [
        {"name": "cakes", "amount": 40},
        {"name": "banana", "amount": 59},
        {"name": "knitting needles", "amount": 13},
        {"name": "white out", "amount": 81},
        {"name": "magnet", "amount": 74},
        {"name": "zebra", "amount": -1},
        {"name": "cow", "amount": 209},
        {"name": "trucks", "amount": 99},
        {"name": "envelope", "amount": 100},
        {"name": "pen", "amount": 25},
        {"name": "paperclip", "amount": 500},
    ]
    table = RelaTable(rows=[{"name": "bowling ball", "amount": 9}])
    table.rows(list_of_objects)
    assert table.export() == list_of_objects


def test_wrong_data_type():
    with pytest.raises(TypeError):
        table = RelaTable(rows=123)
    table = RelaTable()
    with pytest.raises(TypeError):
        table.rows(456)
