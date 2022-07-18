from ..base import ShopifyResource

class Variant(ShopifyResource):
    inventory_item_id: int
    inventory_quantity: int
    sku: str
    tracked: bool
    def save(self) -> Variant: ...
