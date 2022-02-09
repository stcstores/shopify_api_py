"""Methods for interacting with Shopify orders."""

import shopify

from shopify_api_py import request


def get_all_orders() -> list[shopify.Order]:
    """Return a list of all shopify orders."""
    request_method = shopify.Order.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]
