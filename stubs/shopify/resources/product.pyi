import shopify

class Product(
    shopify.ShopifyResource, shopify.mixins.Metafields, shopify.mixins.Events
):
    id: int
    title: str
    body_html: str
    variants: list[shopify.Variant]
    options: list[shopify.Option]
    images: list[shopify.Image]
    tags: str
    vendor: str
    def save(self) -> Product: ...
