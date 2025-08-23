from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, DeleteFileResponseSchema, \
    GetFileResponseSchema


# Приватные методы, которые требуют авторизацию и работают с файлами
class PrivateFilesClient(APIClient):
    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        return self.post("/api/v1/files", data=request.model_dump(exclude={"upload_file"}),
                         files={"upload_file": open(request.upload_file, 'rb')})

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)

    def get_file_api(self, file_id: str) -> Response:
        return self.get(f"/api/v1/files/{file_id}")

    def get_file(self, file_id: str) -> GetFileResponseSchema:
        response = self.get_file_api(file_id)
        return GetFileResponseSchema.model_validate_json(response.text)

    def delete_file_api(self, file_id: str) -> Response:
        return self.delete(f"/api/v1/files/{file_id}")

    def delete_file(self, file_id: str) -> DeleteFileResponseSchema:
        response = self.delete_file_api(file_id)
        return DeleteFileResponseSchema.model_validate_json(response.text)


def get_private_files_client(user: AuthenticationSchema) -> PrivateFilesClient:
    return PrivateFilesClient(client=get_private_http_client(user))
