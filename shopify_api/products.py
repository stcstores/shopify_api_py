"""Methods for interacting with Shopify products."""

import shopify

from shopify_api import exceptions


def get_all_products() -> list[shopify.Product]:
    """Return a list of all shopify products."""
    response = shopify.Product.find()
    products = list(response)
    for _ in range(1000):
        if not response.has_next_page():
            break
        response = shopify.Product.find(from_=response.next_page_url)
        products.extend(list(response))
    else:
        raise exceptions.TooManyPageRequestsError()
    return products
