"""Methods for interacting with Shopify fulfillments."""

import shopify

from shopify_api_py import request


def create_fulfill_order(
    order_id: str | int, location_id: str | int
) -> shopify.ShopifyResource:
    """Create a fulfillment order (Mark an order as fullfilled)."""
    request_method = shopify.Fulfillment.create
    attributes = {"order_id": str(order_id), "location_id": str(location_id)}
    return request.make_request(request_method=request_method, attributes=attributes)
