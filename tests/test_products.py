from unittest.mock import MagicMock, Mock, call, patch

import pytest

from shopify_api import exceptions, products


@pytest.fixture
def mock_shopify():
    with patch("shopify_api.products.shopify") as mock:
        yield mock


@pytest.fixture
def mock_products():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_single_page_products_response(mock_shopify, mock_products):
    response = MagicMock(next_page_url=None)
    response.has_next_page.return_value = False
    response.__iter__.return_value = mock_products
    mock_shopify.Product.find.return_value = response


@pytest.fixture
def mock_multi_page_response_1_products():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_multi_page_response_2_products():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_multi_page_response_3_products():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_multi_page_response_1(mock_shopify, mock_multi_page_response_1_products):
    response = MagicMock(next_page_url="products/1")
    response.has_next_page.return_value = True
    response.__iter__.return_value = mock_multi_page_response_1_products
    return response


@pytest.fixture
def mock_multi_page_response_2(mock_shopify, mock_multi_page_response_2_products):
    response = MagicMock(next_page_url="products/2")
    response.has_next_page.return_value = True
    response.__iter__.return_value = mock_multi_page_response_2_products
    return response


@pytest.fixture
def mock_multi_page_response_3(mock_shopify, mock_multi_page_response_3_products):
    response = MagicMock(next_page_url=None)
    response.has_next_page.return_value = False
    response.__iter__.return_value = mock_multi_page_response_3_products
    return response


@pytest.fixture
def mock_multi_page_products_response(
    mock_shopify,
    mock_multi_page_response_1,
    mock_multi_page_response_2,
    mock_multi_page_response_3,
):
    mock_shopify.Product.find.side_effect = [
        mock_multi_page_response_1,
        mock_multi_page_response_2,
        mock_multi_page_response_3,
    ]


def test_get_all_products_calls_find(mock_shopify, mock_single_page_products_response):
    products.get_all_products()
    mock_shopify.Product.find.assert_called_once_with()


def test_get_all_products_returns_products_single_page(
    mock_shopify, mock_single_page_products_response, mock_products
):
    return_value = products.get_all_products()
    assert return_value == mock_products


def test_get_all_products_returns_products_multi_page(
    mock_shopify,
    mock_multi_page_products_response,
    mock_multi_page_response_1_products,
    mock_multi_page_response_2_products,
    mock_multi_page_response_3_products,
):
    return_value = products.get_all_products()
    assert (
        return_value
        == mock_multi_page_response_1_products
        + mock_multi_page_response_2_products
        + mock_multi_page_response_3_products
    )


def test_get_all_products_requests_all_pages(
    mock_shopify,
    mock_multi_page_products_response,
    mock_multi_page_response_1_products,
    mock_multi_page_response_2_products,
    mock_multi_page_response_3_products,
):
    products.get_all_products()
    mock_shopify.Product.find.assert_has_calls(
        (call(), call(from_="products/1"), call(from_="products/2"))
    )
    assert mock_shopify.Product.find.call_count == 3


def test_get_all_products_stops_after_max_pages(
    mock_shopify, mock_multi_page_response_1
):
    mock_shopify.Product.find.return_value = mock_multi_page_response_1
    with pytest.raises(exceptions.TooManyPageRequestsError):
        products.get_all_products()
