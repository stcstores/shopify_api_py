from unittest.mock import Mock, patch

import pytest
import shopify

from shopify_api import products


@pytest.fixture
def mock_request():
    with patch("shopify_api.products.request") as mock_request:
        yield mock_request


def test_get_all_products_calls_make_request(mock_request):
    products.get_all_products()
    mock_request.make_request.assert_called_once_with(
        request_method=shopify.Product.find
    )


def test_get_all_products_returns_make_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_request.return_value = return_value
    assert products.get_all_products() is return_value
