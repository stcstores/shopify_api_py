from shopify import ShopifyResource, mixins

class Image(ShopifyResource):
    id: int
    product_id: int
    src: str
    variant_ids: list[int]
    def attach_image(self, data: bytes, filename: str | None = ...) -> None: ...
    def save(self) -> Image: ...
