"""Methods for interacting with Shopify products."""

import shopify

from shopify_api import request


def get_all_products() -> list[shopify.ShopifyResource]:
    """Return a list of all shopify products."""
    request_method = shopify.Product.find
    return request.make_request(request_method=request_method)
