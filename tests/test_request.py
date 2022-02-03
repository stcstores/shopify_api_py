from unittest.mock import MagicMock, Mock, call

import pytest

from shopify_api_py import exceptions, request


@pytest.fixture
def mock_request_method():
    return MagicMock()


@pytest.fixture
def mock_resources():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_single_page_resources_response(mock_request_method, mock_resources):
    response = MagicMock(next_page_url=None)
    response.has_next_page.return_value = False
    response.__iter__.return_value = mock_resources
    mock_request_method.return_value = response


@pytest.fixture
def mock_multi_page_response_1_resources():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_multi_page_response_2_resources():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_multi_page_response_3_resources():
    return [Mock(), Mock(), Mock()]


@pytest.fixture
def mock_multi_page_response_1(
    mock_request_method, mock_multi_page_response_1_resources
):
    response = MagicMock(next_page_url="resources/1")
    response.has_next_page.return_value = True
    response.__iter__.return_value = mock_multi_page_response_1_resources
    return response


@pytest.fixture
def mock_multi_page_response_2(
    mock_request_method, mock_multi_page_response_2_resources
):
    response = MagicMock(next_page_url="resources/2")
    response.has_next_page.return_value = True
    response.__iter__.return_value = mock_multi_page_response_2_resources
    return response


@pytest.fixture
def mock_multi_page_response_3(
    mock_request_method, mock_multi_page_response_3_resources
):
    response = MagicMock(next_page_url=None)
    response.has_next_page.return_value = False
    response.__iter__.return_value = mock_multi_page_response_3_resources
    return response


@pytest.fixture
def mock_multi_page_resources_response(
    mock_request_method,
    mock_multi_page_response_1,
    mock_multi_page_response_2,
    mock_multi_page_response_3,
):
    mock_request_method.side_effect = [
        mock_multi_page_response_1,
        mock_multi_page_response_2,
        mock_multi_page_response_3,
    ]


def test_make_request_calls_request_method():
    kwargs = {"a": "b"}
    request_method = Mock()
    request.make_request(request_method=request_method, **kwargs)
    request_method.assert_called_once_with(**kwargs)


def test_make_request_returns_request_method():
    return_value = Mock()
    request_method = Mock(return_value=return_value)
    returned_value = request.make_request(request_method=request_method)
    assert returned_value == return_value


def test_get_all_resources_calls_find(
    mock_request_method, mock_single_page_resources_response
):
    request.make_paginated_request(request_method=mock_request_method)
    mock_request_method.assert_called_once_with()


def test_get_all_resources_returns_resources_single_page(
    mock_request_method, mock_single_page_resources_response, mock_resources
):
    return_value = request.make_paginated_request(request_method=mock_request_method)
    assert return_value == mock_resources


def test_get_all_resources_returns_resources_multi_page(
    mock_request_method,
    mock_multi_page_resources_response,
    mock_multi_page_response_1_resources,
    mock_multi_page_response_2_resources,
    mock_multi_page_response_3_resources,
):
    return_value = request.make_paginated_request(request_method=mock_request_method)
    assert (
        return_value
        == mock_multi_page_response_1_resources
        + mock_multi_page_response_2_resources
        + mock_multi_page_response_3_resources
    )


def test_get_all_resources_requests_all_pages(
    mock_request_method,
    mock_multi_page_resources_response,
    mock_multi_page_response_1_resources,
    mock_multi_page_response_2_resources,
    mock_multi_page_response_3_resources,
):
    request.make_paginated_request(request_method=mock_request_method)
    mock_request_method.assert_has_calls(
        (call(), call(from_="resources/1"), call(from_="resources/2"))
    )
    assert mock_request_method.call_count == 3


def test_get_all_resources_stops_after_max_pages(
    mock_request_method, mock_multi_page_response_1
):
    mock_request_method.return_value = mock_multi_page_response_1
    with pytest.raises(exceptions.TooManyPageRequestsError):
        request.make_paginated_request(request_method=mock_request_method)
