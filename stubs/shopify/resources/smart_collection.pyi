from typing import overload

from shopify import ShopifyResource, collection

class SmartCollection(ShopifyResource):
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> SmartCollection: ...
    @overload
    @classmethod
    def find(cls) -> collection.PaginatedCollection: ...
    def save(self) -> SmartCollection: ...
