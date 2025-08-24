import pytest
from pydantic import BaseModel, EmailStr

from clients.builders.private_http_builder import AuthenticationSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema


class UserData(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def login_user(self) -> AuthenticationSchema:
        return AuthenticationSchema(email=self.email, password=self.password)


@pytest.fixture
def create_user(public_users_client: PublicUsersClient) -> UserData:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserData(request=request, response=response)

@pytest.fixture
def private_users_client(create_user: UserData) -> PrivateUsersClient:
    return get_private_users_client(create_user.login_user)

@pytest.fixture
def public_users_client() -> PublicUsersClient:
    return get_public_users_client()