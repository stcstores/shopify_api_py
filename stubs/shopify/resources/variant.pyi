from ..base import ShopifyResource

class Variant(ShopifyResource):
    inventory_item_id: int
    inventory_quantity: int
