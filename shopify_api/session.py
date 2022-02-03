"""Session manager for the shopify API."""

from pathlib import Path
from typing import Any, Callable, Optional, Union

import shopify
import toml

from .exceptions import LoginCredentialsNotSetError


class ShopifyAPISession:
    """Session manager for the shopify API."""

    SHOP_URL = None
    API_VERSION = None
    API_PASSWORD = None

    CONFIG_FILENAME = ".shopify_api.toml"

    def __enter__(self) -> shopify.Session:
        if not self.__class__.credentails_are_set():
            config_path = self.__class__.find_config_filepath()
            if config_path is not None:
                self.__class__.load_from_config_file(config_file_path=config_path)
        if not self.__class__.credentails_are_set():
            raise LoginCredentialsNotSetError()
        session = shopify.Session(
            shop_url=self.__class__.SHOP_URL,
            version=self.__class__.API_VERSION,
            token=self.__class__.API_PASSWORD,
        )
        shopify.ShopifyResource.activate_session(session)
        return session

    def __exit__(self, exc_type: None, exc_value: None, exc_tb: None) -> None:
        shopify.ShopifyResource.clear_session()

    @classmethod
    def set_login(
        cls,
        shop_url: Optional[str] = None,
        api_version: Optional[str] = None,
        api_password: Optional[str] = None,
    ) -> None:
        """Set required login credentials (shop url, API version and API password)."""
        cls.SHOP_URL = shop_url
        cls.API_VERSION = api_version
        cls.API_PASSWORD = api_password

    @classmethod
    def credentails_are_set(cls) -> bool:
        """Return True if all login credentials are set, otherwise False."""
        if None in (cls.SHOP_URL, cls.API_VERSION, cls.API_PASSWORD):
            return False
        else:
            return True

    @classmethod
    def find_config_filepath(cls) -> Optional[Path]:
        """
        Return the path to a shopify config file or None.

        Recursivly scan backwards from the current working directory and return the
        path to a file matching cls.CONFIG_FILENAME if one exists, otherwise returns
        None.
        """
        path = Path.cwd()
        while path.parent != path:
            config_file = path / cls.CONFIG_FILENAME
            if config_file.exists():
                return config_file
            path = path.parent
        return None

    @classmethod
    def load_from_config_file(cls, config_file_path: Union[Path, str]) -> None:
        """Set login credentials as specified in a toml file located at config_file_path."""
        with open(config_file_path) as f:
            config = toml.load(f)
        cls.set_login(
            shop_url=config.get("SHOP_URL"),
            api_version=config.get("API_VERSION"),
            api_password=config.get("API_PASSWORD"),
        )


def shopify_api_session(func: Callable) -> Callable:
    """Use a shopify API session as a method decorator."""

    def wrapper_shopify_api_session(*args: Any, **kwargs: Any) -> Any:
        with ShopifyAPISession():
            return func(*args, **kwargs)

    return wrapper_shopify_api_session
