from unittest.mock import Mock, patch

import pytest
import shopify

from shopify_api import locations


@pytest.fixture
def mock_request():
    with patch("shopify_api.locations.request") as mock_request:
        yield mock_request


def test_get_all_products_calls_make_paginated_request(mock_request):
    locations.get_inventory_locations()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Location.find
    )


def test_get_all_products_returns_make_paginated_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert locations.get_inventory_locations() is return_value
