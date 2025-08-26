from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.files.private_files_client import PrivateFilesClient
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.files import assert_create_file_response, assert_create_file_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.FILES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@pytest.mark.create
@pytest.mark.files
@pytest.mark.regression
class TestCreateFile:
    @allure.severity(Severity.TRIVIAL)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("User creates the file with correct data")
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_create_file(self, private_files_client_manual_create_file: PrivateFilesClient):
        request = CreateFileRequestSchema()

        response = private_files_client_manual_create_file.create_file_api(request)
        response_json = CreateFileResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateFileResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.TRIVIAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("User creates the file with incorrect data")
    @pytest.mark.errors
    @pytest.mark.parametrize("field, invalid_value, location",
                             [("filename", "", "filename"), ("directory", "", "directory")])
    def test_create_file_with_incorrect_data(self, private_files_client_manual_create_file: PrivateFilesClient,
                                             field, invalid_value, location):
        request_data = {}
        request_data[field] = invalid_value
        request = CreateFileRequestSchema(**request_data)

        response = private_files_client_manual_create_file.create_file_api(request)
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_incorrect_data_response(response_json, invalid_value, location)
