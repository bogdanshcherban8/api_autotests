from functools import lru_cache

from httpx import Client
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_schema import LoginRequestSchema
from clients.authentication.public_authentication_client import get_public_authentication_client

class AuthenticationSchema(BaseModel, frozen=True):
    email: EmailStr
    password: str

#Билдер клиента, чтобы задавать базовую ссылку, авторизацию для приватных методов
@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationSchema)->Client:
    authentication_client = get_public_authentication_client()
    login_api_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_api_request)
    return Client(timeout=100, base_url="http://localhost:8000", headers={"Authorization":f"Bearer {login_response.token.access_token}"})
