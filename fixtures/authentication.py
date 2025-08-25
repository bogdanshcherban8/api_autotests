import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_schema import RefreshResponseSchema, RefreshRequestSchema, \
    LoginResponseSchema, LoginRequestSchema
from clients.authentication.public_authentication_client import PublicAuthenticationClient, \
    get_public_authentication_client



class LoginData(BaseModel):
    request: LoginRequestSchema
    response: LoginResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

@pytest.fixture
def login_user(public_authentication_client:PublicAuthenticationClient):
    request=LoginRequestSchema()
    response=public_authentication_client.login(request)
    return LoginData(request=request, response=response)


@pytest.fixture
def public_authentication_client() -> PublicAuthenticationClient:
    return get_public_authentication_client()

