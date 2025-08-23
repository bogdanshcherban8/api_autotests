from httpx import Response

from clients.api_client import APIClient
from clients.builders.public_http_builder import get_public_http_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema


# Публичный метод, который не требует авторизации и создает пользователя для будущей авторизации
class PublicUsersClient(APIClient):
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    return PublicUsersClient(client=get_public_http_client())
