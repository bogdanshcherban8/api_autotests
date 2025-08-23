from httpx import Response

from clients.api_client import APIClient
from clients.authentication.authentication_schema import LoginRequestSchema, RefreshRequestSchema, LoginResponseSchema, \
    RefreshResponseSchema
from clients.builders.public_http_builder import get_public_http_client


# Публичные методы, которые не требуют авторизацию и работают с авторизацией
class PublicAuthenticationClient(APIClient):
    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post("/api/v1/authentication/login", json=request.model_dump(by_alias=True))

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)

    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        return self.post("/api/v1/authentication/refresh", json=request.model_dump(by_alias=True))

    def refresh(self, request: RefreshRequestSchema) -> RefreshResponseSchema:
        response = self.refresh_api(request)
        return RefreshResponseSchema.model_validate_json(response.text)


def get_public_authentication_client() -> PublicAuthenticationClient:
    return PublicAuthenticationClient(client=get_public_http_client())
