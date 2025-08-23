from httpx import Client

#Билдер клиента, чтобы задавать базовую ссылку для публичных методов
def get_public_http_client() -> Client:
    return Client(timeout=100, base_url="http://localhost:8000")