from __future__ import annotations

from typing import Any

from shopify import ShopifyResource, mixins


class Fulfillment(ShopifyResource, mixins.Metafields, mixins.Events):
    @classmethod
    def create(cls, attributes: dict[str, Any]) -> Fulfillment:
        ...
