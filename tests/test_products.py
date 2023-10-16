from unittest.mock import Mock, patch

import pytest
import shopify
from pyactiveresource.connection import ResourceNotFound

from shopify_api_py import exceptions, products


@pytest.fixture
def mock_request():
    with patch("shopify_api_py.products.request") as mock_request:
        yield mock_request


@pytest.fixture
def location_id():
    return 4981561849


@pytest.fixture
def inventory_item_id():
    return 19846461654


@pytest.fixture
def new_stock_level():
    return 5


@pytest.fixture
def product_id():
    return 68156156486


@pytest.fixture
def variant_id():
    return 96513515615


@pytest.fixture
def collection_id():
    return 684616516516


@pytest.fixture
def collect_id():
    return 41646161666


@pytest.fixture
def image_url():
    return "https://nothing.com"


def test_get_all_products_calls_make_paginated_request(mock_request):
    products.get_all_products()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Product.find
    )


def test_get_all_products_returns_make_paginated_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert products.get_all_products() is return_value


def test_get_all_variants_calls_make_paginated_request(mock_request):
    products.get_all_variants()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Variant.find
    )


def test_get_all_variants_returns_make_paginated_request_return_value(mock_request):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert products.get_all_variants() is return_value


def test_set_stock_level_calls_make_request(
    mock_request, location_id, inventory_item_id, new_stock_level
):
    products.set_stock_level(
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        new_stock_level=new_stock_level,
    )
    mock_request.make_request.assert_called_once_with(
        request_method=shopify.InventoryLevel.set,
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        available=new_stock_level,
    )


def test_set_stock_level_returns_request_response(
    mock_request, location_id, inventory_item_id, new_stock_level
):
    response = Mock()
    mock_request.make_request.return_value = response
    return_value = products.set_stock_level(
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        new_stock_level=new_stock_level,
    )
    assert return_value == response


@patch("shopify_api_py.products.set_stock_level")
def test_update_variant_stock_calls_set_stock_level(
    mock_set_stock_level, location_id, inventory_item_id, new_stock_level
):
    variant = Mock(inventory_item_id=inventory_item_id)
    products.update_variant_stock(
        variant=variant, location_id=location_id, new_stock_level=new_stock_level
    )
    mock_set_stock_level.assert_called_once_with(
        location_id=location_id,
        inventory_item_id=inventory_item_id,
        new_stock_level=new_stock_level,
    )


@patch("shopify_api_py.products.set_stock_level")
def test_update_variant_stock_returns_response(
    mock_set_stock_level, location_id, inventory_item_id, new_stock_level
):
    set_stock_level_response = Mock()
    mock_set_stock_level.return_value = set_stock_level_response
    variant = Mock(inventory_item_id=inventory_item_id)
    return_value = products.update_variant_stock(
        variant=variant, location_id=location_id, new_stock_level=new_stock_level
    )
    assert return_value == set_stock_level_response


@patch("shopify_api_py.products.shopify.InventoryItem.find")
def test_get_inventory_item_by_id_requests_inventory_item(
    mock_inventory_item_find, inventory_item_id
):
    products.get_inventory_item_by_id(inventory_item_id)
    mock_inventory_item_find.assert_called_once_with(id_=inventory_item_id)


@patch("shopify_api_py.products.shopify.InventoryItem.find")
def test_get_inventory_item_by_id_returns_inventory_item(
    mock_inventory_item_find, inventory_item_id
):
    mock_return_value = Mock()
    mock_inventory_item_find.return_value = mock_return_value
    returned_value = products.get_inventory_item_by_id(inventory_item_id)
    assert returned_value == mock_return_value


@patch("shopify_api_py.products.get_inventory_item_by_id")
def test_set_customs_information_calls_get_inventory_item_by_id(
    mock_get_inventory_item_by_id, inventory_item_id
):
    mock_inventory_item = Mock()
    mock_inventory_item.save.return_value = True
    mock_get_inventory_item_by_id.return_value = mock_inventory_item
    products.set_customs_information(
        inventory_item_id=inventory_item_id,
        country_of_origin_code="GB",
        hs_code="999999",
    )
    mock_get_inventory_item_by_id.assert_called_once_with(inventory_item_id)


@patch("shopify_api_py.products.get_inventory_item_by_id")
def test_set_customs_information_sets_country_code_of_origin(
    mock_get_inventory_item_by_id, inventory_item_id
):
    mock_inventory_item = Mock()
    mock_inventory_item.save.return_value = True
    mock_get_inventory_item_by_id.return_value = mock_inventory_item
    products.set_customs_information(
        inventory_item_id=inventory_item_id,
        country_of_origin_code="GB",
        hs_code="999999",
    )
    assert mock_inventory_item.country_code_of_origin == "GB"


@patch("shopify_api_py.products.get_inventory_item_by_id")
def test_set_customs_information_sets_hs_code(
    mock_get_inventory_item_by_id, inventory_item_id
):
    mock_inventory_item = Mock()
    mock_inventory_item.save.return_value = True
    mock_get_inventory_item_by_id.return_value = mock_inventory_item
    products.set_customs_information(
        inventory_item_id=inventory_item_id,
        country_of_origin_code="GB",
        hs_code="999999",
    )
    assert mock_inventory_item.harmonized_system_code == "999999"


@patch("shopify_api_py.products.get_inventory_item_by_id")
def test_set_customs_information_saves_inventory_item(
    mock_get_inventory_item_by_id, inventory_item_id
):
    mock_inventory_item = Mock()
    mock_inventory_item.save.return_value = True
    mock_get_inventory_item_by_id.return_value = mock_inventory_item
    products.set_customs_information(
        inventory_item_id=inventory_item_id,
        country_of_origin_code="GB",
        hs_code="999999",
    )
    mock_inventory_item.save.assert_called_once_with()


@patch("shopify_api_py.products.get_inventory_item_by_id")
def test_set_customs_information_raises_for_invalid_request(
    mock_get_inventory_item_by_id, inventory_item_id
):
    mock_inventory_item = Mock()
    mock_inventory_item.save.return_value = False
    mock_get_inventory_item_by_id.return_value = mock_inventory_item
    with pytest.raises(exceptions.ResponseError):
        products.set_customs_information(
            inventory_item_id=inventory_item_id,
            country_of_origin_code="GB",
            hs_code="999999",
        )


def test_create_options():
    variation_matrix = {
        "Colour": ["Red", "Green", "Blue"],
        "Size": ["Small", "Medium", "Large"],
    }
    returned_value = products.create_options(variation_matrix=variation_matrix)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 2
    assert isinstance(returned_value[0], shopify.Option)
    assert returned_value[0].name == "Colour"
    assert returned_value[0].values == variation_matrix["Colour"]
    assert isinstance(returned_value[1], shopify.Option)
    assert returned_value[1].name == "Size"
    assert returned_value[1].values == variation_matrix["Size"]


def test_create_variation():
    sku = "JFJ-JFJ-LSL"
    option_values = ["Red", "Small"]
    barcode = "843897435"
    grams = 5
    price = 5.50
    returned_value = products.create_variation(
        sku=sku, option_values=option_values, barcode=barcode, grams=grams, price=price
    )
    assert isinstance(returned_value, shopify.Variant)
    assert returned_value.sku == sku
    assert returned_value.tracked is True
    assert returned_value.barcode == barcode
    assert returned_value.weight_unit == "g"
    assert returned_value.price == price
    assert returned_value.option1 == option_values[0]
    assert returned_value.option2 == option_values[1]


def test_create_variation_sets_tracked():
    sku = "JFJ-JFJ-LSL"
    option_values = ["Red", "Small"]
    barcode = "843897435"
    grams = 5
    price = 5.50
    returned_value = products.create_variation(
        sku=sku,
        option_values=option_values,
        barcode=barcode,
        grams=grams,
        price=price,
        tracked=False,
    )
    assert isinstance(returned_value, shopify.Variant)
    assert returned_value.tracked is False


@pytest.fixture
def mock_image():
    mock_image = Mock()
    mock_image.save.return_value = True
    return mock_image


@patch("shopify_api_py.products.shopify.Image")
def test_add_product_image_creates_a_new_image(
    mock_Image, mock_image, product_id, image_url
):
    mock_Image.return_value = mock_image
    returned_value = products.add_product_image(
        product_id=product_id, image_url=image_url
    )
    mock_Image.assert_called_once_with()
    assert returned_value == mock_image
    assert mock_image.product_id == product_id
    assert mock_image.src == image_url


@patch("shopify_api_py.products.shopify.Image")
def test_add_product_image_returns_an_image(
    mock_Image, mock_image, product_id, image_url
):
    mock_Image.return_value = mock_image
    returned_value = products.add_product_image(
        product_id=product_id, image_url=image_url
    )
    assert returned_value == mock_image


@patch("shopify_api_py.products.shopify.Image")
def test_add_product_image_sets_product_id(
    mock_Image, mock_image, product_id, image_url
):
    mock_Image.return_value = mock_image
    products.add_product_image(product_id=product_id, image_url=image_url)
    assert mock_image.product_id == product_id
    assert mock_image.src == image_url


@patch("shopify_api_py.products.shopify.Image")
def test_add_product_image_sets_image_url(
    mock_Image, mock_image, product_id, image_url
):
    mock_Image.return_value = mock_image
    products.add_product_image(product_id=product_id, image_url=image_url)
    assert mock_image.src == image_url


@patch("shopify_api_py.products.shopify.Image")
def test_add_product_image_sets_variant_ids(
    mock_Image, mock_image, product_id, image_url
):
    mock_Image.return_value = mock_image
    variant_ids = [1861818, 61564615, 894416156]
    products.add_product_image(
        product_id=product_id, image_url=image_url, variant_ids=variant_ids
    )
    assert mock_image.variant_ids == variant_ids


@patch("shopify_api_py.products.shopify.Image")
def test_add_product_image_raises_for_unsuccesful_request(
    mock_Image, mock_image, product_id, image_url
):
    mock_Image.return_value = mock_image
    mock_image.save.return_value = False
    with pytest.raises(exceptions.ResponseError):
        products.add_product_image(product_id=product_id, image_url=image_url)


@pytest.fixture
def mock_product():
    mock_product = Mock()
    mock_product.save.return_value = True
    return mock_product


@pytest.fixture
def product_title():
    return "Product Title"


@pytest.fixture
def product_description():
    return "<p>Product Description</p>"


@pytest.fixture
def product_vendor():
    return "Unbranded"


@pytest.fixture
def product_tags():
    return ["Tag1", "Tag2"]


@pytest.fixture
def product_options():
    return products.create_options(
        {
            "Size": ["Small", "Medium"],
            "Colour": ["Red", "Green"],
        }
    )


@pytest.fixture
def product_variants():
    return [
        products.create_variation(
            sku="SKU_1",
            barcode="651616168",
            grams=50,
            price=5.50,
            option_values=["Small", "Red"],
        ),
        products.create_variation(
            sku="SKU_2",
            barcode="651616168",
            grams=50,
            price=5.50,
            option_values=["Small", "Green"],
        ),
        products.create_variation(
            sku="SKU_3",
            barcode="651616168",
            grams=50,
            price=5.50,
            option_values=["Medium", "Red"],
        ),
        products.create_variation(
            sku="SKU_4",
            barcode="651616168",
            grams=50,
            price=5.50,
            option_values=["Medium", "Green"],
        ),
    ]


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_a_product_object(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
    )
    mock_Product.assert_called_once()
    assert returned_value == mock_product


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_sets_title(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
    )
    assert returned_value.title == product_title


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_sets_description(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
    )
    assert returned_value.body_html == product_description


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_sets_vendor(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
    product_tags,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
        tags=product_tags,
    )
    assert returned_value.vendor == product_vendor


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_sets_tags(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
    product_tags,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
        tags=product_tags,
    )
    assert returned_value.tags == "Tag1,Tag2"


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_sets_options(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
    product_variants,
    product_options,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
        variants=product_variants,
        options=product_options,
    )
    assert returned_value.options == product_options


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_sets_variants(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
    product_variants,
    product_options,
):
    mock_Product.return_value = mock_product
    returned_value = products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
        variants=product_variants,
        options=product_options,
    )
    assert returned_value.variants == product_variants


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_saves_product(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
):
    mock_Product.return_value = mock_product
    products.create_product(
        title=product_title,
        body_html=product_description,
        vendor=product_vendor,
    )
    mock_product.save.assert_called_once()


@patch("shopify_api_py.products.shopify.Product")
def test_create_product_creates_raises_for_unsucessful_response(
    mock_Product,
    mock_product,
    product_title,
    product_description,
    product_vendor,
):
    mock_Product.return_value = mock_product
    mock_product.save.return_value = False
    with pytest.raises(exceptions.ResponseError):
        products.create_product(
            title=product_title,
            body_html=product_description,
            vendor=product_vendor,
        )


@patch("shopify_api_py.products.shopify.Product")
def test_get_product_by_id_requests_product(mock_Product, product_id):
    products.get_product_by_id(product_id)
    mock_Product.find.assert_called_once_with(id_=product_id)


@patch("shopify_api_py.products.shopify.Product")
def test_get_product_by_id_returns_product(mock_Product, product_id):
    mock_product = Mock()
    mock_Product.find.return_value = mock_product
    returned_value = products.get_product_by_id(product_id)
    assert returned_value == mock_product


@patch("shopify_api_py.products.shopify.Product")
def test_get_product_by_id_raises_product_not_found_error(mock_Product, product_id):
    mock_Product.find.side_effect = ResourceNotFound
    with pytest.raises(exceptions.ProductNotFoundError):
        products.get_product_by_id(product_id)


@patch("shopify_api_py.products.shopify.Variant")
def test_get_variant_by_id_requests_product(mock_Variant, variant_id):
    products.get_variant_by_id(variant_id)
    mock_Variant.find.assert_called_once_with(id_=variant_id)


@patch("shopify_api_py.products.shopify.Variant")
def test_get_variant_by_id_returns_product(mock_Variant, variant_id):
    mock_variant = Mock()
    mock_Variant.find.return_value = mock_variant
    returned_value = products.get_variant_by_id(variant_id)
    assert returned_value == mock_variant


@patch("shopify_api_py.products.shopify.Variant")
def test_get_variant_by_id_raises_product_not_found_error(mock_Variant, variant_id):
    mock_Variant.find.side_effect = ResourceNotFound
    with pytest.raises(exceptions.VariantNotFoundError):
        products.get_variant_by_id(variant_id)


@patch("shopify_api_py.products.shopify.InventoryItem")
def test_get_inventory_item_by_id_requests_product(
    mock_InventoryItem, inventory_item_id
):
    products.get_inventory_item_by_id(inventory_item_id)
    mock_InventoryItem.find.assert_called_once_with(id_=inventory_item_id)


@patch("shopify_api_py.products.shopify.InventoryItem")
def test_get_inventory_item_by_id_returns_product(
    mock_InventoryItem, inventory_item_id
):
    mock_variant = Mock()
    mock_InventoryItem.find.return_value = mock_variant
    returned_value = products.get_inventory_item_by_id(inventory_item_id)
    assert returned_value == mock_variant


@patch("shopify_api_py.products.shopify.InventoryItem")
def test_get_inventory_item_by_id_raises_product_not_found_error(
    mock_InventoryItem, inventory_item_id
):
    mock_InventoryItem.find.side_effect = ResourceNotFound
    with pytest.raises(exceptions.InventoryItemNotFoundError):
        products.get_inventory_item_by_id(inventory_item_id)


def test_get_all_custom_collections_calls_make_paginated_request(mock_request):
    products.get_all_custom_collections()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.CustomCollection.find
    )


def test_get_all_custom_collections_returns_make_paginated_request_return_value(
    mock_request,
):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert products.get_all_custom_collections() is return_value


@patch("shopify_api_py.products.shopify.CustomCollection")
def test_get_custom_collection_by_id_requests_custom_collection(
    mock_CustomCollection, collection_id
):
    products.get_custom_collection_by_id(collection_id)
    mock_CustomCollection.find.assert_called_once_with(id_=collection_id)


@patch("shopify_api_py.products.shopify.CustomCollection")
def test_get_custom_collection_by_id_returns_custom_collection(
    mock_CustomCollection, collection_id
):
    mock_custom_collection = Mock()
    mock_CustomCollection.find.return_value = mock_custom_collection
    returned_value = products.get_custom_collection_by_id(collection_id)
    assert returned_value == mock_custom_collection


@patch("shopify_api_py.products.shopify.CustomCollection")
def test_get_custom_collection_by_id_raises_custom_collection_not_found_error(
    mock_CustomCollection, collection_id
):
    mock_CustomCollection.find.side_effect = ResourceNotFound
    with pytest.raises(exceptions.CustomCollectionNotFoundError):
        products.get_custom_collection_by_id(collection_id)


def test_get_all_smart_collections_calls_make_paginated_request(mock_request):
    products.get_all_smart_collections()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.SmartCollection.find
    )


def test_get_all_smart_collections_returns_make_paginated_request_return_value(
    mock_request,
):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert products.get_all_smart_collections() is return_value


@patch("shopify_api_py.products.shopify.SmartCollection")
def test_get_smart_collection_by_id_requests_smart_collection(
    mock_SmartCollection, collection_id
):
    products.get_smart_collection_by_id(collection_id)
    mock_SmartCollection.find.assert_called_once_with(id_=collection_id)


@patch("shopify_api_py.products.shopify.SmartCollection")
def test_get_smart_collection_by_id_returns_smart_collection(
    mock_SmartCollection, collection_id
):
    mock_smart_collection = Mock()
    mock_SmartCollection.find.return_value = mock_smart_collection
    returned_value = products.get_smart_collection_by_id(collection_id)
    assert returned_value == mock_smart_collection


@patch("shopify_api_py.products.shopify.SmartCollection")
def test_get_smart_collection_by_id_raises_smart_collection_not_found_error(
    mock_SmartCollection, collection_id
):
    mock_SmartCollection.find.side_effect = ResourceNotFound
    with pytest.raises(exceptions.SmartCollectionNotFoundError):
        products.get_smart_collection_by_id(collection_id)


def test_get_all_collects_calls_make_paginated_request(mock_request):
    products.get_all_collects()
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Collect.find
    )


def test_get_all_collects_returns_make_paginated_request_return_value(
    mock_request,
):
    return_value = Mock()
    mock_request.make_paginated_request.return_value = return_value
    assert products.get_all_collects() is return_value


@patch("shopify_api_py.products.shopify.Collect")
def test_get_collect_by_id_requests_collect(mock_Collect, collect_id):
    products.get_collect_by_id(collect_id)
    mock_Collect.find.assert_called_once_with(id_=collect_id)


@patch("shopify_api_py.products.shopify.Collect")
def test_get_collect_by_id_returns_collect(mock_Collect, collect_id):
    mock_collect = Mock()
    mock_Collect.find.return_value = mock_collect
    returned_value = products.get_collect_by_id(collect_id)
    assert returned_value == mock_collect


@patch("shopify_api_py.products.shopify.Collect")
def test_collect_by_id_raises_collect_not_found_error(mock_Collect, collect_id):
    mock_Collect.find.side_effect = ResourceNotFound
    with pytest.raises(exceptions.CollectNotFoundError):
        products.get_collect_by_id(collect_id)


@patch("shopify_api_py.products.shopify.Collect")
def test_add_product_to_collection_creates_a_collect(
    mock_Collect, product_id, collection_id
):
    mock_collect = Mock()
    mock_Collect.return_value = mock_collect
    products.add_product_to_collection(
        product_id=product_id, collection_id=collection_id
    )
    mock_Collect.assert_called_once_with()
    mock_collect.save.assert_called_once_with()


@patch("shopify_api_py.products.shopify.Collect")
def test_add_product_to_collection_sets_product_id(
    mock_Collect, product_id, collection_id
):
    mock_collect = Mock()
    mock_Collect.return_value = mock_collect
    products.add_product_to_collection(
        product_id=product_id, collection_id=collection_id
    )
    assert mock_collect.product_id == product_id


@patch("shopify_api_py.products.shopify.Collect")
def test_add_product_to_collection_sets_collection_id(
    mock_Collect, product_id, collection_id
):
    mock_collect = Mock()
    mock_Collect.return_value = mock_collect
    products.add_product_to_collection(
        product_id=product_id, collection_id=collection_id
    )
    assert mock_collect.collection_id == collection_id


@patch("shopify_api_py.products.shopify.Collect")
def test_add_product_to_collection_raises_ResponseError_incase_of_exception(
    mock_Collect, product_id, collection_id
):
    mock_collect = Mock()
    mock_collect.save.side_effect = Exception("Test exception")
    mock_Collect.return_value = mock_collect
    with pytest.raises(exceptions.ResponseError):
        products.add_product_to_collection(
            product_id=product_id, collection_id=collection_id
        )


@patch("shopify_api_py.products.shopify.Collect")
def test_add_product_to_collection_raises_ResponseError_incase_of_failed_response(
    mock_Collect, product_id, collection_id
):
    mock_collect = Mock()
    mock_collect.save.return_value = False
    mock_Collect.return_value = mock_collect
    with pytest.raises(exceptions.ResponseError):
        products.add_product_to_collection(
            product_id=product_id, collection_id=collection_id
        )


@patch("shopify_api_py.products.shopify.Collect")
def test_remove_product_from_collection_finds_collects(
    mock_Collect, product_id, collection_id
):
    mock_Collect.find.return_value = [Mock()]
    products.remove_product_from_collection(
        product_id=product_id, collection_id=collection_id
    )
    mock_Collect.find.assert_called_once_with(
        product_id=product_id, collection_id=collection_id
    )


@patch("shopify_api_py.products.shopify.Collect")
def test_remove_product_from_collection_raises_if_no_collects_are_found(
    mock_Collect, product_id, collection_id
):
    mock_Collect.find.return_value = []
    with pytest.raises(exceptions.ResponseError):
        products.remove_product_from_collection(
            product_id=product_id, collection_id=collection_id
        )


@patch("shopify_api_py.products.shopify.Collect")
def test_remove_product_from_collection_calls_destroy_on_collects(
    mock_Collect, product_id, collection_id
):
    mock_Collect.find.return_value = [Mock(), Mock(), Mock()]
    products.remove_product_from_collection(
        product_id=product_id, collection_id=collection_id
    )
    for value in mock_Collect.find.return_value:
        value.destroy.assert_called_once_with()


@patch("shopify_api_py.products.shopify.Collect")
def test_remove_product_from_collection_raises_ResponseError_incase_of_exception_destroying_collect(
    mock_Collect, product_id, collection_id
):
    mock_Collect.find.return_value = [Mock(), Mock(), Mock()]
    mock_Collect.find.return_value[1].destroy.side_effect = Exception("Test exception")
    with pytest.raises(exceptions.ResponseError):
        products.remove_product_from_collection(
            product_id=product_id, collection_id=collection_id
        )


def test_get_products_in_custom_collection_finds_collects(mock_request, collection_id):
    products.get_products_in_custom_collection(collection_id=collection_id)
    mock_request.make_paginated_request.assert_called_once_with(
        request_method=shopify.Collect.find, kwargs={"collection_id": collection_id}
    )


def test_get_products_in_custom_collection_returns_product_ids(
    mock_request, collection_id
):
    mock_collects = [Mock(), Mock(), Mock()]
    mock_request.make_paginated_request.return_value = mock_collects
    returned_value = products.get_products_in_custom_collection(
        collection_id=collection_id
    )
    assert returned_value == [mock.product_id for mock in mock_collects]
