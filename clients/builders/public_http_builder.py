from httpx import Client

from clients.event_hooks import curl_event_hook, log_request_event_hook, log_response_event_hook
from config import settings


# Билдер клиента, чтобы задавать базовую ссылку для публичных методов
def get_public_http_client() -> Client:
    return Client(timeout=settings.http_client.timeout, base_url=settings.http_client.url,
                  event_hooks={"request": [curl_event_hook, log_request_event_hook],
                               "response": [log_response_event_hook]})
