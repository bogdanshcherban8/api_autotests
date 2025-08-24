from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.users.users_schema import UpdateUserRequestSchema, \
    GetUserResponseSchema, UpdateUserResponseSchema


# Приватные методы, которые требуют авторизацию и работают с юзером
class PrivateUsersClient(APIClient):
    def get_user_me_api(self) -> Response:
        return self.get("/api/v1/users/me")

    def get_user_me(self) -> GetUserResponseSchema:
        response = self.get_user_me_api()
        return GetUserResponseSchema.model_validate_json(response.text)

    def get_user_by_id_api(self, user_id: str) -> Response:
        return self.get(f"/api/v1/users/{user_id}")

    def get_user_by_id(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_by_id_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        return self.patch(f"/api/v1/users/{user_id}", json=request.model_dump(by_alias=True))

    def update_user(self, user_id: str, request: UpdateUserRequestSchema) -> UpdateUserResponseSchema:
        response = self.update_user_api(user_id, request)
        return UpdateUserResponseSchema.model_validate_json(response.text)

    def delete_user_api(self, user_id: str) -> Response:
        return self.delete(f"/api/v1/users/{user_id}")


def get_private_users_client(user: AuthenticationSchema) -> PrivateUsersClient:
    return PrivateUsersClient(client=get_private_http_client(user))
