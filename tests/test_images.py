from unittest.mock import Mock, patch

import pytest
import shopify

from shopify_api_py import images


@pytest.fixture
def product_id():
    return 6824330264716


@pytest.fixture
def mock_request():
    with patch("shopify_api_py.images.request") as mock_request:
        yield mock_request


def test_get_all_orders_calls_make_paginated_request(mock_request, product_id):
    images.get_images_for_product(product_id=product_id)
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Image.find, product_id=product_id
    )


def test_get_all_orders_returns_make_paginated_request_return_value(
    mock_request, product_id
):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert images.get_images_for_product(product_id=product_id) is return_value
