import shopify

class Product(
    shopify.ShopifyResource, shopify.mixins.Metafields, shopify.mixins.Events
):
    title: str
    body: str
    variants: list[shopify.Variant]
    options: list[shopify.Option]
    def save(self) -> Product: ...
