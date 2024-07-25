import pytest
from python_of_sale import get_order_dictionary, get_order_total_price

def test_get_order_dictionary():
    assert get_order_dictionary("2 kebab 1 soda 4 water") == {"kebab": 2, "soda": 1, "water": 4}
    assert get_order_dictionary("2 cake 4 juice 2 water") == {"cake": 2, "juice": 4, "water": 2}
    assert get_order_dictionary("2 cake juice 4 water") == {}
    assert get_order_dictionary("cake juice water") == {}
    assert get_order_dictionary("2 4 2 1") == {}
    assert get_order_dictionary("") == {}

def test_get_order_total_price():
    order_dictionary = {"kebab": 2, "soda": 1, "water": 4}
    available_offers_dictionary = {"kebab": 2, "soda": 4, "water": 8}
    assert get_order_total_price(order_dictionary, available_offers_dictionary) == 40

    order_dictionary = {"cake": 2, "juice": 4, "water": 2}
    available_offers_dictionary = {"cake": 8, "juice": 4, "water": 2}
    assert get_order_total_price(order_dictionary, available_offers_dictionary) == 36

    order_dictionary = {}
    available_offers_dictionary = {"cake": 8, "juice": 4, "water": 2}
    assert get_order_total_price(order_dictionary, available_offers_dictionary) == 0

    order_dictionary = {"cake": 2, "juice": 4, "water": 2}
    available_offers_dictionary = {}
    with pytest.raises(ValueError, match="not included in the provided available offers dictionary"):
        get_order_total_price(order_dictionary, available_offers_dictionary)

pytest.main()