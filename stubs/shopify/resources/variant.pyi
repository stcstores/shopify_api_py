from ..base import ShopifyResource

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
