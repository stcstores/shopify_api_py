import shopify

class Option(shopify.ShopifyResource, shopify.mixins.Metafields, shopify.mixins.Events):
    name: str
    values: list[str]
    def save(self) -> Option: ...
