from shopify import mixins

from ..base import ShopifyResource

class Product(ShopifyResource, mixins.Metafields, mixins.Events): ...
