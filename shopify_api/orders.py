"""Methods for interacting with Shopify orders."""

import shopify

from shopify_api import request


def get_all_orders() -> list[shopify.ShopifyResource]:
    """Return a list of all shopify orders."""
    request_method = shopify.Order.find
    return request.make_request(request_method=request_method)
