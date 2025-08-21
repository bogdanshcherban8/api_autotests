from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import AuthenticationUserDict, get_private_http_client


class CreateFileRequestDict(TypedDict):
    filename: str
    directory: str
    upload_file: str


class FilesClient(APIClient):
    def create_file_api(self, request: CreateFileRequestDict) -> Response:
        return self.post("/api/v1/files", data=request, files={"upload_file": open(request['upload_file'], 'rb')})

    def get_file_api(self, file_id: str) -> Response:
        return self.get(f"/api/v1/files/{file_id}")

    def delete_file_api(self, file_id: str)->Response:
        return self.delete(f"/api/v1/files/{file_id}")

def get_files_client(user:AuthenticationUserDict)->FilesClient:
    return FilesClient(client=get_private_http_client(user))