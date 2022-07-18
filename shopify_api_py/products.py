"""Methods for interacting with Shopify products."""

import itertools

import shopify

from shopify_api_py import request


def get_all_products() -> list[shopify.Product]:
    """Return a list of all shopify products."""
    request_method = shopify.Product.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def get_all_variants() -> list[shopify.Variant]:
    """Return a list of all shopify variants."""
    request_method = shopify.Variant.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def set_stock_level(
    location_id: int, inventory_item_id: int, new_stock_level: int
) -> shopify.ShopifyResource:
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
) -> shopify.ShopifyResource:
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


def create_product() -> shopify.Product:
    options = []
    variants = []
    variations = {
        "Size": ["Small", "Medium", "Large"],
        "Colour": ["Red", "Green", "Blue"],
    }
    for option_name, values in variations.items():
        option = shopify.Option()
        option.name = option_name
        option.values = values
        options.append(option)
    for i, variation in enumerate(itertools.product(*list(variations.values())), 1):
        variant = shopify.Variant()
        variant.sku = f"TEST_SKU_{i}"
        variant.tracked = True
        for i, value in enumerate(variation, 1):
            setattr(variant, f"option{i}", value)
        variants.append(variant)
    product = shopify.Product()
    product.title = "API TEST"
    product.body = "Test Description"
    product.variants = variants
    product.options = options

    response = product.save()
    print(product, response)
    return product
