from typing import overload

from shopify import ShopifyResource, collection

class Collect(ShopifyResource):
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> Collect: ...
    @overload
    @classmethod
    def find(cls) -> collection.PaginatedCollection: ...
    def save(self) -> Collect: ...
