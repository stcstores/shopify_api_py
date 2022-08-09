from typing import overload

from shopify import ShopifyResource, collection

class Variant(ShopifyResource):
    id: int
    inventory_item_id: int
    inventory_quantity: int
    sku: str
    barcode: str
    grams: int
    weight_unit: str
    price: float
    tracked: bool
    def save(self) -> Variant: ...
    @overload  # type: ignore
    @classmethod
    def find(cls, id_: str | int | None) -> Variant: ...
    @overload
    @classmethod
    def find(cls) -> collection.PaginatedCollection: ...
