from unittest.mock import Mock, patch

import pytest
import shopify

from shopify_api_py import orders


@pytest.fixture
def mock_request():
    with patch("shopify_api_py.orders.request") as mock_request:
        yield mock_request


def test_get_all_orders_calls_make_paginated_request(mock_request):
    orders.get_all_orders()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Order.find
    )


def test_get_all_orders_returns_make_paginated_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert orders.get_all_orders() is return_value
