import pytest
from pydantic import BaseModel

from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.files.private_files_client import PrivateFilesClient, get_private_files_client
from fixtures.users import UserData


class FileData(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema


@pytest.fixture
def create_file(private_files_client: PrivateFilesClient) -> FileData:
    request = CreateFileRequestSchema()
    response = private_files_client.create_file(request)
    return FileData(request=request, response=response)


@pytest.fixture
def private_files_client(create_user: UserData) -> PrivateFilesClient:
    return get_private_files_client(create_user.login_user)


@pytest.fixture
def private_files_client_manual_create_file(create_user: UserData) -> PrivateFilesClient:
    return get_private_files_client(create_user.login_user)