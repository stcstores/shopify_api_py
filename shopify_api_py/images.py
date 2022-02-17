"""Methods for interacting with Shopify products."""

import shopify

from shopify_api_py import request


def get_images_for_product(product_id: str | int) -> list[shopify.Image]:
    """Return a list of all shopify variants."""
    request_method = shopify.Image.find
    return request.make_paginated_request(
        request_method=request_method, product_id=int(product_id)
    )  # type: ignore[return-value]
