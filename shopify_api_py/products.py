"""Methods for interacting with Shopify products."""

import shopify

from shopify_api_py import exceptions, request


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


def get_inventory_item_by_id(inventory_item_id: int) -> shopify.InventoryItem:
    """Return the `shopify.InventoryItem` object matching the inventory item ID.

    Args:
        inventory_item_id (int): ID of the inventory item to be returned.

    Returns:
        shopify.InventoryItem: The inventory item with the id inventory_item_id.
    """
    return shopify.InventoryItem.find(inventory_item_id)  # type: ignore[return-value]


def set_customs_information(
    inventory_item_id: int, country_of_origin_code: str, hs_code: str
) -> None:
    """Set the customs information for an inventory item.

    Args:
        inventory_item_id (int): The ID of the inventory item to update.
        country_of_origin_code (str): The two letter country code of the country of
            origin.
        hs_code (str): The Harmonised system code.

    Raises:
        exceptions.ResponseError: If an error is returned to the request.
    """
    inventory_item = get_inventory_item_by_id(inventory_item_id)
    inventory_item.country_code_of_origin = country_of_origin_code
    inventory_item.harmonized_system_code = hs_code
    response = inventory_item.save()
    if response is not True:
        raise exceptions.ResponseError("Error setting customs information")


def create_options(variation_matrix: dict[str, list[str]]) -> list[shopify.Option]:
    """Return a list of `shopify.Option` objects based on a variation matrix.

    Args:
        variation_matrix (dict[str, list[str]]): A dictionary where the keys are the
            name of a variation attribute and the values are a list of variation values.

    Returns:
        list[shopify.Option]: A list containing `shopify.Option` objects representing
            the variations described in variation_matrix for use in creating variation
            products.
    """
    options = []
    for variation_attribute, variation_values in variation_matrix.items():
        option = shopify.Option()
        option.name = variation_attribute
        option.values = variation_values
        options.append(option)
    return options


def create_variation(
    sku: str,
    option_values: list[str],
    barcode: str,
    grams: int,
    price: float,
    tracked: bool = True,
) -> shopify.Variant:
    """Return a new `shopify.Variant` object for use in creating new products.

    Args:
        sku (str): The SKU of the new variant.
        option_values (list[str]): A list of variation attribute values identifying the
            variation. Order must match the order of options passed to create_product.
        barcode (str): The variant's barcode.
        grams (int): The weight of the variant in grams.
        price (float): The price at which the variant will be sold.
        tracked (bool, optional): If True stock levels will be tracked for the
            variant. Defaults to True.

    Returns:
        shopify.Variant: A new variant object that can be passed to create_product.
    """
    variant = shopify.Variant()
    variant.sku = sku
    variant.tracked = tracked
    variant.barcode = barcode
    variant.grams = grams
    variant.weight_unit = "g"
    variant.price = price
    for i, value in enumerate(option_values, 1):
        setattr(variant, f"option{i}", value)
    return variant


def add_product_image(
    product_id: int, image_url: str, variant_ids: list[int] | None = None
) -> shopify.Image:
    """Add a new image to a product.

    Args:
        product_id (int): The ID of the product the image will be added to.
        image_url (str): The source URL of the image.
        variant_ids (list[int] | None, optional): A list of Variant IDs the image will
            be added to or None the image will be added to or None if the image applies
            to the product only. Defaults to None.

    Raises:
        exceptions.ResponseError: If the request does not return sucessful.

    Returns:
        shopify.Image: The new product image.
    """
    image = shopify.Image()
    image.product_id = product_id
    image.src = image_url
    if variant_ids is not None:
        image.variant_ids = variant_ids
    response = image.save()
    if response is False:
        raise exceptions.ResponseError("Error adding image.")
    return image


def create_product(
    title: str,
    body_html: str,
    vendor: str,
    options: list[shopify.Option] | None = None,
    variants: list[shopify.Variant] | None = None,
    tags: list[str] | None = None,
) -> shopify.Product:
    """Create a new product on Shopify.

    Args:
        title (str): The product's name.
        body_html (str): The product's description as HTML.
        vendor (str): The vendor (brand) of the product.
        options (list[shopify.Option] | None, optional): If the product is a variation
            product a list of `shopify.Option` objects must be passed describing the
            variation options. Defaults to None.
        variants (list[shopify.Variant] | None, optional): A list of `shopify.Variant`
            objects describing the product's variations. Use None for single products.
            If variants is not None then the options kwarg must also not be None.
            Defaults to None.
        tags (list[str] | None, optional): A list of product tags to use on the product.
            Defaults to None.

    Raises:
        exceptions.ResponseError: If the product creation request does not return
            successful.

    Returns:
        shopify.Product: The newly created product.
    """
    product = shopify.Product()
    product.title = title
    product.body_html = body_html
    product.vendor = vendor
    if variants is not None and options is not None:
        product.variants = variants
        product.options = options
    if tags is not None:
        product.tags = ",".join(tags)
    response = product.save()
    if response is False:
        raise exceptions.ResponseError("Error creating product.")
    return product
