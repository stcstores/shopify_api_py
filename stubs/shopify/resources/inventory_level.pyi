from collections.abc import Mapping

from ..base import ShopifyResource

class InventoryLevel(ShopifyResource):
    @classmethod
    def adjust(
        cls, location_id: int, inventory_item_id: int, available_adjustment: int
    ) -> InventoryLevel: ...
    @classmethod
    def set(
        cls,
        location_id: int,
        inventory_item_id: int,
        available: int,
        disconnect_if_necessary: bool = ...,
        **kwargs: Mapping
    ) -> InventoryLevel: ...
