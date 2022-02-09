from unittest.mock import Mock, patch

import pytest
import shopify

from shopify_api_py import fulfillment


@pytest.fixture
def mock_request():
    with patch("shopify_api_py.fulfillment.request") as mock_request:
        yield mock_request


@pytest.fixture
def order_id():
    return 3972772266124


@pytest.fixture
def location_id():
    return 3478823862412


def test_get_all_orders_calls_make_request(mock_request, order_id, location_id):
    fulfillment.create_fulfill_order(order_id=order_id, location_id=location_id)
    mock_request.make_request.assert_called_once_with(
        request_method=shopify.Fulfillment.create,
        attributes={"order_id": str(order_id), "location_id": str(location_id)},
    )


def test_get_all_orders_returns_make_request_return_value(
    mock_request, order_id, location_id
):
    return_value = Mock()
    mock_request.make_request.return_value = return_value
    returned_value = fulfillment.create_fulfill_order(
        order_id=order_id, location_id=location_id
    )
    assert returned_value is return_value
