from typing import overload

from shopify import ShopifyResource, collection

class InventoryItem(ShopifyResource):
    country_code_of_origin: str
    harmonized_system_code: str
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> InventoryItem: ...
    @overload
    @classmethod
    def find(cls) -> collection.PaginatedCollection: ...
    def save(self) -> InventoryItem: ...
