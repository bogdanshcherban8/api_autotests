import allure
from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from tools.routes import APIRoutes


# Приватные методы, которые требуют авторизацию и работают с файлами
class PrivateFilesClient(APIClient):
    @allure.step("Create file")
    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        return self.post(APIRoutes.FILES, data=request.model_dump(exclude={"upload_file"}),
                         files = {"upload_file": request.upload_file.read_bytes()})

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)

    @allure.step("Get file by id {file_id}")
    def get_file_api(self, file_id: str) -> Response:
        return self.get(f"{APIRoutes.FILES}/{file_id}")

    def get_file(self, file_id: str) -> GetFileResponseSchema:
        response = self.get_file_api(file_id)
        return GetFileResponseSchema.model_validate_json(response.text)

    @allure.step("Delete file by id {file_id}")
    def delete_file_api(self, file_id: str) -> Response:
        return self.delete(f"{APIRoutes.FILES}/{file_id}")


def get_private_files_client(user: AuthenticationSchema) -> PrivateFilesClient:
    return PrivateFilesClient(client=get_private_http_client(user))
