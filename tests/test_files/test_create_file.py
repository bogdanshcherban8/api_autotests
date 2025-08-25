from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.files.private_files_client import PrivateFilesClient
from tools.assertions.files import assert_create_file_response, assert_create_file_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.create
@pytest.mark.files
@pytest.mark.regression
class TestCreateFile:
    def test_create_file(self, private_files_client_manual_create_file: PrivateFilesClient):
        request = CreateFileRequestSchema()

        response = private_files_client_manual_create_file.create_file_api(request)
        response_json = CreateFileResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateFileResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_json)

    @pytest.mark.errors
    @pytest.mark.parametrize("field, invalid_value, location",
                             [("filename", "", "filename"), ("directory", "", "directory")])
    def test_create_file_with_incorrect_data(self, private_files_client_manual_create_file: PrivateFilesClient,
                                                 field, invalid_value, location):
        request_data={}
        request_data[field]=invalid_value
        request = CreateFileRequestSchema(**request_data)

        response = private_files_client_manual_create_file.create_file_api(request)
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_incorrect_data_response(response_json, invalid_value, location)
