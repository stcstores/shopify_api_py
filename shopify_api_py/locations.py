"""Methods for interacting with Shopify locations."""

import shopify

from shopify_api_py import request


def get_inventory_locations() -> list[shopify.ShopifyResource]:
    """Return a list of all shopify products."""
    request_method = shopify.Location.find
    return request.make_paginated_request(request_method=request_method)
