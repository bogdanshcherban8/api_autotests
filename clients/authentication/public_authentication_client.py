import allure
from httpx import Response

from clients.api_client import APIClient
from clients.authentication.authentication_schema import LoginRequestSchema, RefreshRequestSchema, LoginResponseSchema, \
    RefreshResponseSchema
from clients.builders.public_http_builder import get_public_http_client
from tools.routes import APIRoutes


# Публичные методы, которые не требуют авторизацию и работают с авторизацией
class PublicAuthenticationClient(APIClient):
    @allure.step("Authenticate user")
    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post(f"{APIRoutes.AUTHENTICATION}/login", json=request.model_dump(by_alias=True))

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)

    @allure.step("Refresh user token")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        return self.post(f"{APIRoutes.AUTHENTICATION}/refresh", json=request.model_dump(by_alias=True))

    def refresh(self, request: RefreshRequestSchema) -> RefreshResponseSchema:
        response = self.refresh_api(request)
        return RefreshResponseSchema.model_validate_json(response.text)


def get_public_authentication_client() -> PublicAuthenticationClient:
    return PublicAuthenticationClient(client=get_public_http_client())
