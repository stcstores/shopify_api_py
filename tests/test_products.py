from unittest.mock import Mock, patch

import pytest
import shopify

from shopify_api import products


@pytest.fixture
def mock_request():
    with patch("shopify_api.products.request") as mock_request:
        yield mock_request


@pytest.fixture
def location_id():
    return 4981561849


@pytest.fixture
def inventory_item_id():
    return 19846461654


@pytest.fixture
def new_stock_level():
    return 5


def test_get_all_products_calls_make_request(mock_request):
    products.get_all_products()
    mock_request.make_request.assert_called_once_with(
        request_method=shopify.Product.find
    )


def test_get_all_products_returns_make_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_request.return_value = return_value
    assert products.get_all_products() is return_value


def test_get_all_variants_calls_make_request(mock_request):
    products.get_all_variants()
    mock_request.make_request.assert_called_once_with(
        request_method=shopify.Variant.find
    )


def test_get_all_variants_returns_make_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_request.return_value = return_value
    assert products.get_all_variants() is return_value


def test_set_stock_level_calls_make_request(
    mock_request, location_id, inventory_item_id, new_stock_level
):
    products.set_stock_level(
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        new_stock_level=new_stock_level,
    )
    mock_request.make_request.assert_called_once_with(
        request_method=shopify.InventoryLevel.set,
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        available=new_stock_level,
    )


def test_set_stock_level_returns_request_response(
    mock_request, location_id, inventory_item_id, new_stock_level
):
    response = Mock()
    mock_request.make_request.return_value = response
    return_value = products.set_stock_level(
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        new_stock_level=new_stock_level,
    )
    assert return_value == response


@patch("shopify_api.products.set_stock_level")
def test_update_variant_stock_calls_set_stock_level(
    mock_set_stock_level, location_id, inventory_item_id, new_stock_level
):
    variant = Mock(inventory_item_id=inventory_item_id)
    products.update_variant_stock(
        variant=variant, location_id=location_id, new_stock_level=new_stock_level
    )
    mock_set_stock_level.assert_called_once_with(
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        new_stock_level=new_stock_level,
    )


@patch("shopify_api.products.set_stock_level")
def test_update_variant_stock_returns_response(
    mock_set_stock_level, location_id, inventory_item_id, new_stock_level
):
    set_stock_level_response = Mock()
    mock_set_stock_level.return_value = set_stock_level_response
    variant = Mock(inventory_item_id=inventory_item_id)
    return_value = products.update_variant_stock(
        variant=variant, location_id=location_id, new_stock_level=new_stock_level
    )
    assert return_value == set_stock_level_response
