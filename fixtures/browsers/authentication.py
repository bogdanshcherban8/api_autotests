import pytest

from clients.authentication.public_authentication_client import PublicAuthenticationClient, \
    get_public_authentication_client


@pytest.fixture
def public_authentication_client() -> PublicAuthenticationClient:
    return get_public_authentication_client()
