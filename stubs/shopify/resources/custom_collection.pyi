from typing import overload

from shopify import ShopifyResource, collection

class CustomCollection(ShopifyResource):
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> CustomCollection: ...
    @overload
    @classmethod
    def find(cls) -> collection.PaginatedCollection: ...
    def save(self) -> CustomCollection: ...
