from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema
from clients.files.files_schema import GetFileResponseSchema
from clients.files.private_files_client import PrivateFilesClient
from fixtures.files import FileData
from tools.assertions.files import assert_get_file_response, assert_get_file_with_incorrect_file_id_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema
@pytest.mark.get
@pytest.mark.users
@pytest.mark.regression
class TestGetFileById:
    def test_get_file_by_id(self, private_files_client:PrivateFilesClient, create_file:FileData):
        response = private_files_client.get_file_api(create_file.response.file.id)
        response_json = GetFileResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetFileResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_file_response(response_json, create_file.response.file)

    @pytest.mark.errors
    def test_get_file_with_incorrect_file_id(self, private_files_client:PrivateFilesClient):
        response = private_files_client.get_file_api(file_id="incorrect-file-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_json)


