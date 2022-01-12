class Session:
    api_key: str | None
    secret: str | None
    protocol: str | None
    myshopify_domain: str | None
    port: int | None

    url: str | None
    token: str | None
    version: str | None
    def __init__(
        self,
        shop_url: str | None,
        version: str | None = ...,
        token: str | None = ...,
        access_scopes: str | None = ...,
    ) -> None: ...
