from typing import TypedDict

from httpx import Response

from api_client.api_client import APIClient
class RegistrationRequestDict(TypedDict):
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    def create_user_api(self, request: RegistrationRequestDict) -> Response:
        return self.post("/api/v1/users", json=request)