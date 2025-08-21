from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.builders.public_http_builder import get_public_http_client


class Token(TypedDict):
    tokenType: str
    accessToken: str
    refreshToken: str


class LoginResponseDict(TypedDict):
    token: Token


class LoginRequestDict(TypedDict):
    email: str
    password: str


class RefreshRequestDict(TypedDict):
    refreshToken: str


class AuthenticationClient(APIClient):
    def login_api(self, request: LoginRequestDict) -> Response:
        return self.post("/api/v1/authentication/login", json=request)

    def refresh_token_api(self, request: RefreshRequestDict):
        return self.post("/api/v1/authentication/refresh", json=request)

    def login(self, request: LoginRequestDict) -> LoginResponseDict:
        response = self.login_api(request)
        return response.json()

def get_authentication_client() -> AuthenticationClient:
    return AuthenticationClient(client=get_public_http_client())
