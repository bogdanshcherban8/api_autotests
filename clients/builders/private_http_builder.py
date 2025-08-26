from functools import lru_cache

from httpx import Client
from pydantic import BaseModel, EmailStr
from config import settings
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.authentication.public_authentication_client import get_public_authentication_client
from clients.event_hooks import curl_event_hook, log_request_event_hook, log_response_event_hook


class AuthenticationSchema(BaseModel, frozen=True):
    email: EmailStr
    password: str


# Билдер клиента, чтобы задавать базовую ссылку, авторизацию для приватных методов
@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationSchema) -> Client:
    authentication_client = get_public_authentication_client()
    login_api_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_api_request)
    return Client(timeout=settings.http_client.timeout, base_url=settings.http_client.url,
                  headers={"Authorization": f"Bearer {login_response.token.access_token}"},
                  event_hooks={"request": [curl_event_hook, log_request_event_hook], "response": [log_response_event_hook]})
