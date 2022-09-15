"""Methods for interacting with Shopify products."""

import shopify
from pyactiveresource.connection import ResourceNotFound

from shopify_api_py import exceptions, request


def get_all_products() -> list[shopify.Product]:
    """Return a list of all shopify products."""
    request_method = shopify.Product.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def get_product_by_id(product_id: int) -> shopify.Product:
    """Return the product with ID product_id.

    Args:
        product_id (int): ID of the product to return.

    Raises:
        exceptions.ProductNotFoundError: If no product is found.

    Returns:
        shopify.Product: shopify.Product: The Shopify product with the ID product_id.
    """
    try:
        return shopify.Product.find(id_=product_id)
    except ResourceNotFound:
        raise exceptions.ProductNotFoundError(product_id) from None


def get_all_variants() -> list[shopify.Variant]:
    """Return a list of all shopify variants."""
    request_method = shopify.Variant.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def get_variant_by_id(variant_id: int) -> shopify.Variant:
    """Return the variant with ID variant_id.

    Args:
        variant_id (int): ID of the variant to return.

    Raises:
        exceptions.VariantNotFoundError: If no variant is found.

    Returns:
        shopify.Variant: The Shopify variant with the ID variant_id.
    """
    try:
        return shopify.Variant.find(id_=variant_id)
    except ResourceNotFound:
        raise exceptions.VariantNotFoundError(variant_id) from None


def get_inventory_item_by_id(inventory_item_id: int) -> shopify.InventoryItem:
    """Return the inventory item with ID variant_id.

    Args:
        inventory_item_id (int): ID of the inventory item to return.

    Raises:
        exceptions.VariantNotFoundError: If no inventory item is found.

    Returns:
        shopify.Variant: The Shopify inventory item with the ID inventory_item_id.
    """
    try:
        return shopify.InventoryItem.find(id_=inventory_item_id)
    except ResourceNotFound:
        raise exceptions.InventoryItemNotFoundError(inventory_item_id) from None


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


def get_all_custom_collections() -> list[shopify.CustomCollection]:
    """Return a list of all shopify custom collections."""
    request_method = shopify.CustomCollection.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def get_custom_collection_by_id(collection_id: int) -> shopify.CustomCollection:
    """Return the custom collection with ID collection_id.

    Args:
        collection_id (int): ID of the custom collection to return.

    Raises:
        exceptions.CustomCollectionNotFoundError: If no custom collection is found.

    Returns:
        shopify.CustomCollection: The Shopify custom collection with the ID collection_id.
    """
    try:
        return shopify.CustomCollection.find(id_=collection_id)
    except ResourceNotFound:
        raise exceptions.CustomCollectionNotFoundError(collection_id) from None


def get_all_smart_collections() -> list[shopify.SmartCollection]:
    """Return a list of all shopify smart collections."""
    request_method = shopify.SmartCollection.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def get_smart_collection_by_id(collection_id: int) -> shopify.SmartCollection:
    """Return the smart collection with ID collection_id.

    Args:
        collection_id (int): ID of the smart collection to return.

    Raises:
        exceptions.SmartCollectionNotFoundError: If no smart collection is found.

    Returns:
        shopify.SmartCollection: The Shopify smart collection with the ID collection_id.
    """
    try:
        return shopify.SmartCollection.find(id_=collection_id)
    except ResourceNotFound:
        raise exceptions.SmartCollectionNotFoundError(collection_id) from None


def get_all_collects() -> list[shopify.Collect]:
    """Return a list of all shopify collects."""
    request_method = shopify.Collect.find
    return request.make_paginated_request(request_method=request_method)  # type: ignore[return-value]


def get_collect_by_id(collect_id: int) -> shopify.Collect:
    """Return the collect with ID collect_id.

    Args:
        collect_id (int): ID of the collect to return.

    Raises:
        exceptions.CollectNotFoundError: If no collect is found.

    Returns:
        shopify.Collect: The Shopify collect with the ID collect_id.
    """
    try:
        return shopify.Collect.find(id_=collect_id)
    except ResourceNotFound:
        raise exceptions.CollectNotFoundError(collect_id) from None


def add_product_to_collection(product_id: int, collection_id: int) -> None:
    """Add a product to a custom collection.

    Args:
        product_id (int): ID of the product to add.
        collection_id (int): ID of the collection to add the product to.

    Raises:
        exceptions.ResponseError: If an error is creating when requesting creation of
            the new Collect.
    """
    collect = shopify.Collect()
    collect.product_id = product_id
    collect.collection_id = collection_id
    try:
        response = collect.save()
    except Exception:
        raise exceptions.ResponseError("Error adding product to collection.")
    if not response:
        raise exceptions.ResponseError("Error adding product to collection.")


def remove_product_from_collection(product_id: int, collection_id: int) -> None:
    """Remove a product from a collection.

    Args:
        product_id (int): The ID of the product to remove.
        collection_id (int): The ID of the collection to be removed from.

    Raises:
        exceptions.ResponseError: If no Collect matching the product and collection
            indicated is found.
    """
    collects = shopify.Collect.find(product_id=product_id, collection_id=collection_id)
    if len(collects) == 0:
        raise exceptions.ResponseError("No matching Collect found.")
    else:
        for collect in collects:
            try:
                collect.destroy()
            except Exception:
                raise exceptions.ResponseError(
                    "Error removing product from collection."
                )


def get_products_in_custom_collection(collection_id: int) -> list[int]:
    """Return the IDs of all products in a custom collection.

    Args:
        collection_id (int): ID of the collection.

    Returns:
        list[int]: List of IDs of products in the collection.
    """
    request_method = shopify.Collect.find
    collects: list[shopify.Collect] = request.make_paginated_request(request_method=request_method, kwargs={"collection_id": collection_id})  # type: ignore[return-value, assignment]
    return [collect.product_id for collect in collects]
