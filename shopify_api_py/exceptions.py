"""Exceptions for the shopify_api_py package."""

from typing import Any, Mapping


class LoginCredentialsNotSetError(ValueError):
    """Exception raised when creating an API session without credentials set."""

    def __init__(self, *args: list[Any], **kwargs: Mapping[str, Any]) -> None:
        """Exception raised when creating an API session without credentials set."""
        super().__init__("SHOP_URL, API_VERSION and API_PASSWORD must be set.")


class TooManyPageRequestsError(Exception):
    """Exception raised when a method requests too many pages from a paginated endpoint."""

    def __init__(self, *args: list[Any], **kwargs: Mapping[str, Any]) -> None:
        """Exception raised when a method requests too many pages from a paginated endpoint."""
        super().__init__("Too many pages requested.")


class ResponseError(Exception):
    """Exception raised wthen a request returns a non success response."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Exception raised wthen a request returns a non success response."""
        super().__init__(*args, **kwargs)


class ResourceNotFoundError(Exception):
    """Exception raised when a non-existant resource is requested."""

    def __init__(self, resource_type: str, resource_id: int | str) -> None:
        """Exception raised when a non-existant resource is requested."""
        super().__init__(f"{resource_type} with ID {resource_id} not found.")


class ProductNotFoundError(ResourceNotFoundError):
    """Exception raised when a non-existant product is requested."""

    def __init__(self, product_id: int | str) -> None:
        """Exception raised when a non-existant product is requested."""
        super().__init__(resource_type="Product", resource_id=product_id)


class VariantNotFoundError(ResourceNotFoundError):
    """Exception raised when a non-existant variant is requested."""

    def __init__(self, variant_id: int | str) -> None:
        """Exception raised when a non-existant variant is requested."""
        super().__init__(resource_type="Product", resource_id=variant_id)


class InventoryItemNotFoundError(ResourceNotFoundError):
    """Exception raised when a non-existant inventory item is requested."""

    def __init__(self, inventory_item_id: int | str) -> None:
        """Exception raised when a non-existant inventory item is requested."""
        super().__init__(resource_type="Inventory Item", resource_id=inventory_item_id)


class CustomCollectionNotFoundError(ResourceNotFoundError):
    """Exception raised when a non-existant custom collection is requested."""

    def __init__(self, collection_id: int | str) -> None:
        """Exception raised when a non-existant custom collection is requested."""
        super().__init__(resource_type="Custom Collection", resource_id=collection_id)


class SmartCollectionNotFoundError(ResourceNotFoundError):
    """Exception raised when a non-existant smart collection is requested."""

    def __init__(self, collection_id: int | str) -> None:
        """Exception raised when a non-existant smart collection is requested."""
        super().__init__(resource_type="Smart Collection", resource_id=collection_id)


class CollectNotFoundError(ResourceNotFoundError):
    """Exception raised when a non-existant collect is requested."""

    def __init__(self, collect_id: int | str) -> None:
        """Exception raised when a non-existant collect is requested."""
        super().__init__(resource_type="Collect", resource_id=collect_id)
