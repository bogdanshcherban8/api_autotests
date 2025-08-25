from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.files.private_files_client import PrivateFilesClient
from fixtures.files import FileData
from tools.assertions.files import assert_file_not_found_response, \
    assert_get_file_with_incorrect_file_id_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.delete
@pytest.mark.files
@pytest.mark.regression
class TestDeleteFile:
    def test_delete_file(self, private_files_client:PrivateFilesClient, create_file:FileData):
        response = private_files_client.delete_file_api(create_file.response.file.id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_get_file = private_files_client.get_file_api(create_file.response.file.id)
        response_get_file_json = InternalErrorResponseSchema.model_validate_json(response_get_file.text)

        validate_json_schema(instance=response_get_file_json, schema=InternalErrorResponseSchema)

        assert_status_code(response_get_file.status_code, HTTPStatus.NOT_FOUND)
        assert_file_not_found_response(response_get_file_json)

    @pytest.mark.errors
    def test_delete_file_with_incorrect_data(self, private_files_client:PrivateFilesClient, create_file:FileData):
        response = private_files_client.delete_file_api(file_id="incorrect-file-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_json)