from typing import overload

from shopify import ShopifyResource, collection

class Collect(ShopifyResource):
    id: int
    product_id: int
    collection_id: int
    position: int
    sort_value: str
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> Collect: ...
    @overload
    @classmethod
    def find(cls) -> collection.PaginatedCollection: ...
    @overload
    @classmethod
    def find(cls, collection_id: str | int) -> collection.PaginatedCollection: ...
    @overload
    @classmethod
    def find(cls, product_id: str | int) -> collection.PaginatedCollection: ...
    @overload
    @classmethod
    def find(
        cls, collection_id: str | int, product_id: str | int
    ) -> collection.PaginatedCollection: ...
    def save(self) -> Collect: ...
