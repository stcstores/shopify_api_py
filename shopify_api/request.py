"""Methods for making Shopify API requests."""

from typing import Any, Callable

import shopify

from shopify_api import exceptions


def make_request(
    request_method: Callable[..., shopify.ShopifyResource], **kwargs: Any
) -> shopify.ShopifyResource:
    """Make a single page shopify request."""
    response = request_method(**kwargs)
    return response


def make_paginated_request(
    request_method: Callable[..., shopify.collection.PaginatedCollection], **kwargs: Any
) -> list[shopify.ShopifyResource]:
    """Make a multi page shopify request."""
    response = request_method(**kwargs)
    items = list(response)
    for _ in range(1000):
        if not response.has_next_page():
            break
        kwargs["from_"] = response.next_page_url
        response = request_method(**kwargs)
        items.extend(list(response))
    else:
        raise exceptions.TooManyPageRequestsError()
    return items
