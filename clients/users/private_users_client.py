from typing import TypedDict

from httpx import Response

from api_client.api_client import APIClient

class UpdateUserRequestDict(TypedDict):
    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None
class PrivateUsersClient(APIClient):
    def get_user_me_api(self)->Response:
        return self.get("/api/v1/users/me")
    def get_user_id_api(self, user_id: str)->Response:
        return self.get(f"/api/v1/users/{user_id}")
    def update_user_api(self, user_id: str, request: UpdateUserRequestDict)->Response:
        return self.patch(f"/api/v1/users/{user_id}", json=request)
    def delete_user_api(self, user_id: str)->Response:
        return self.delete(f"/api/v1/users/{user_id}")