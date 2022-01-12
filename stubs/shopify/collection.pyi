from pyactiveresource.collection import Collection

class PaginatedCollection(Collection):
    next_page_url: str | None
    previous_page_page_url: str | None
    def has_previous_page(self) -> bool: ...
    def has_next_page(self) -> bool: ...
