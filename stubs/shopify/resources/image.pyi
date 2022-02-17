from shopify import ShopifyResource, mixins

class Image(ShopifyResource):
    def attach_image(self, data: bytes, filename: str | None = ...) -> None: ...
