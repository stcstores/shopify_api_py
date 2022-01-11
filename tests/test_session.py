from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import toml

from shopify_api import exceptions, session


@pytest.fixture(autouse=True)
def temp_cwd(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


@pytest.fixture
def mock_shopify():
    with patch("shopify_api.session.shopify") as mock:
        yield mock


@pytest.fixture
def mock_shopify_session(mock_shopify):
    session = Mock()
    mock_shopify.Session.return_value = session
    return session


@pytest.fixture
def shop_url():
    return "mock-shop.shopify.com"


@pytest.fixture
def api_version():
    return "2021-10-mock"


@pytest.fixture
def api_password():
    return "Mock-API-password"


@pytest.fixture(autouse=True)
def clean_shopify_api_session():
    yield
    session.ShopifyAPISession.SHOP_URL = None
    session.ShopifyAPISession.API_VERSION = None
    session.ShopifyAPISession.API_PASSWORD = None
    session.ShopifyAPISession.CONFIG_FILENAME = ".shopify_api.toml"
    print("Cleaned shopify session")


@pytest.fixture
def set_shopify_session_config(shop_url, api_version, api_password):
    session.ShopifyAPISession.SHOP_URL = shop_url
    session.ShopifyAPISession.API_VERSION = api_version
    session.ShopifyAPISession.API_PASSWORD = api_password


@pytest.fixture
def config_file(shop_url, api_version, api_password):
    data = {
        "SHOP_URL": shop_url,
        "API_VERSION": api_version,
        "API_PASSWORD": api_password,
    }
    path = Path.cwd() / session.ShopifyAPISession.CONFIG_FILENAME
    with open(path, "w") as f:
        toml.dump(data, f)
    return path


@pytest.mark.parametrize(
    "shop_url_set,api_version_set,api_password_set,expected",
    [
        (False, False, False, False),
        (False, False, True, False),
        (False, True, False, False),
        (True, False, False, False),
        (True, True, False, False),
        (True, False, True, False),
        (False, True, True, False),
        (True, True, True, True),
    ],
)
def test_credentials_are_set_method(
    shop_url,
    api_version,
    api_password,
    shop_url_set,
    api_version_set,
    api_password_set,
    expected,
):
    if shop_url_set is True:
        session.ShopifyAPISession.SHOP_URL = shop_url
    if api_version_set is True:
        session.ShopifyAPISession.API_VERSION = api_version
    if api_password_set is True:
        session.ShopifyAPISession.API_PASSWORD = api_password
    assert session.ShopifyAPISession.credentails_are_set() is expected


def test_raises_exception_when_called_without_credentials(mock_shopify):
    with pytest.raises(exceptions.LoginCredentialsNotSetError):
        with session.ShopifyAPISession():
            pass


def test_shopify_session_context_manager_creates_session(
    mock_shopify, mock_shopify_session, set_shopify_session_config
):
    with session.ShopifyAPISession():
        pass
    mock_shopify.Session.assert_called_once_with(
        shop_url=session.ShopifyAPISession.SHOP_URL,
        version=session.ShopifyAPISession.API_VERSION,
        token=session.ShopifyAPISession.API_PASSWORD,
    )


def test_shopify_session_context_manager_activates_session(
    mock_shopify, mock_shopify_session, set_shopify_session_config
):
    with session.ShopifyAPISession():
        pass
    mock_shopify.ShopifyResource.activate_session.assert_called_once_with(
        mock_shopify_session
    )


def test_shopify_session_context_manager_closes_session(
    mock_shopify, mock_shopify_session, set_shopify_session_config
):
    with session.ShopifyAPISession():
        pass
    mock_shopify.ShopifyResource.clear_session.assert_called_once()


def test_set_login_method_sets_shop_url(shop_url):
    session.ShopifyAPISession.set_login(shop_url=shop_url)
    assert session.ShopifyAPISession.SHOP_URL == shop_url


def test_set_login_method_sets_api_version(api_version):
    session.ShopifyAPISession.set_login(api_version=api_version)
    assert session.ShopifyAPISession.API_VERSION == api_version


def test_set_login_method_sets_api_password(api_password):
    session.ShopifyAPISession.set_login(api_password=api_password)
    assert session.ShopifyAPISession.API_PASSWORD == api_password


def test_find_config_filepath_returns_config_file_in_cwd(temp_cwd, config_file):
    path = session.ShopifyAPISession.find_config_filepath()
    assert path == temp_cwd / session.ShopifyAPISession.CONFIG_FILENAME


def test_find_config_filepath_returns_None_without_config_file_in_cwd():
    path = session.ShopifyAPISession.find_config_filepath()
    assert path is None


def test_load_from_config_file_sets_shop_url(config_file, shop_url):
    session.ShopifyAPISession.load_from_config_file(config_file)
    assert session.ShopifyAPISession.SHOP_URL == shop_url


def test_load_from_config_file_sets_api_version(config_file, api_version):
    session.ShopifyAPISession.load_from_config_file(config_file)
    assert session.ShopifyAPISession.API_VERSION == api_version


def test_load_from_config_file_sets_api_password(config_file, api_password):
    session.ShopifyAPISession.load_from_config_file(config_file)
    assert session.ShopifyAPISession.API_PASSWORD == api_password


def test_enter_method_loads_credentials_from_file_if_not_set(
    mock_shopify, config_file, shop_url, api_version, api_password
):
    with session.ShopifyAPISession():
        pass
    mock_shopify.Session.assert_called_once_with(
        shop_url=shop_url,
        version=api_version,
        token=api_password,
    )


def test_enter_method_does_not_load_credentials_if_already_set(
    mock_shopify, config_file
):
    temp_value = "tmp_value"
    session.ShopifyAPISession.SHOP_URL = temp_value
    session.ShopifyAPISession.API_VERSION = temp_value
    session.ShopifyAPISession.API_PASSWORD = temp_value
    with session.ShopifyAPISession():
        pass
    assert session.ShopifyAPISession.SHOP_URL == temp_value
    assert session.ShopifyAPISession.API_VERSION == temp_value
    assert session.ShopifyAPISession.API_PASSWORD == temp_value
