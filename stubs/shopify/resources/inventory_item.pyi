from typing import overload

from shopify import ShopifyResource, collection

class InventoryItem(ShopifyResource):
    country_code_of_origin: str
    harmonized_system_code: str
    @staticmethod
    def find(inventory_item_id: int) -> InventoryItem: ...  # type: ignore
    def save(self) -> InventoryItem: ...
