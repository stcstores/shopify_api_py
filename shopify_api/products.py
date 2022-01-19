"""Methods for interacting with Shopify products."""

import shopify

from shopify_api import request


def get_all_products() -> list[shopify.ShopifyResource]:
    """Return a list of all shopify products."""
    request_method = shopify.Product.find
    return request.make_request(request_method=request_method)


def get_all_variants() -> list[shopify.ShopifyResource]:
    """Return a list of all shopify variants."""
    request_method = shopify.Variant.find
    return request.make_request(request_method=request_method)


def set_stock_level(
    location_id: int, inventory_item_id: int, new_stock_level: int
) -> list[shopify.ShopifyResource]:
    """Set the stock level for a variant and location."""
    request_method = shopify.InventoryLevel.set
    kwargs = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": new_stock_level,
    }
    return request.make_request(request_method=request_method, **kwargs)


def update_variant_stock(
    variant: shopify.Variant, location_id: int, new_stock_level: int
) -> list[shopify.ShopifyResource] | None:
    """
    Update the stock level of a variant.

    If the updated stock level matches variant.inventory_quantity do nothing and return
    None.
    """
    response = set_stock_level(
        location_id=location_id,
        inventory_item_id=variant.inventory_item_id,
        new_stock_level=new_stock_level,
    )
    variant.inventory_quantity = new_stock_level
    return response
