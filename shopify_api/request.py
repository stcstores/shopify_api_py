"""Methods for making Shopify API requests."""

from typing import Any, Callable

import shopify

from shopify_api import exceptions


def make_request(
    request_method: Callable, **kwargs: dict[str, Any]
) -> list[shopify.ShopifyResource]:
    """Return a list of all shopify products."""
    response = request_method(**kwargs)
    products = list(response)
    for _ in range(1000):
        if not response.has_next_page():
            break
        kwargs["from_"] = response.next_page_url
        response = request_method(**kwargs)
        products.extend(list(response))
    else:
        raise exceptions.TooManyPageRequestsError()
    return products
