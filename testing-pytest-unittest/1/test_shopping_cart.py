from unittest.mock import Mock

import pytest

from shopping_cart import ShoppingCart
from item_database import ItemDatabase


# Fixtures Section

@pytest.fixture
def cart():
    # All setup and logic for setup cart here...
    cart = ShoppingCart(1)
    return cart


# Tests Section

def test_can_add_item_to_cart(cart):
    cart.add('apple')
    assert cart.size() == 1


def test_when_item_added_then_cart_contains_item(cart):
    apple = 'apple'
    cart.add(apple)
    assert apple in cart.get_items()


def test_when_add_more_than_max_items_should_fail(cart):
    cart.add('apple')
    with pytest.raises(OverflowError):
        cart.add('orange')


def test_can_get_total_price(cart):
    apple = 'apple'
    cart.add(apple)
    price_map = {
        apple: 1.0,
    }
    
    def mock_get_item(item: str):
        if item == 'apple':
            return 1.0
        elif item == 'orange':
            return 2.0
    
    item_database = ItemDatabase()
    # item_database.get = Mock(return_value=1)
    item_database.get = Mock(side_effect=mock_get_item)
    
    assert cart.get_total_price(item_database) == sum(price_map.values())
