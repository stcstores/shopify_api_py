from typing import overload

import shopify

class Product(
    shopify.ShopifyResource, shopify.mixins.Metafields, shopify.mixins.Events
):
    id: int
    title: str
    body_html: str
    variants: list[shopify.Variant]
    options: list[shopify.Option]
    images: list[shopify.Image]
    tags: str
    vendor: str
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> Product: ...
    @overload
    @classmethod
    def find(cls) -> shopify.collection.PaginatedCollection: ...
    def save(self) -> Product: ...
