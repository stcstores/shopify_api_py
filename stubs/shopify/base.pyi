from typing import Any, Mapping

import shopify.mixins as mixins
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource.collection import Collection
from shopify.collection import PaginatedCollection

from .session import Session

class ShopifyResource(ActiveResource, mixins.Countable):
    def __init__(
        self, attributes: Any | None = ..., prefix_options: Any | None = ...
    ): ...
    @classmethod
    def activate_session(cls, session: Session) -> None: ...
    @classmethod
    def clear_session(cls) -> None: ...
    @classmethod
    def find(
        cls, id_: str | None = ..., from_: str | None = ..., **kwargs: Mapping[str, Any]
    ) -> PaginatedCollection: ...
