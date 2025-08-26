from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.files.private_files_client import PrivateFilesClient
from fixtures.files import FileData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.files import assert_file_not_found_response, \
    assert_get_file_with_incorrect_file_id_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.FILES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@pytest.mark.delete
@pytest.mark.files
@pytest.mark.regression
class TestDeleteFile:
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.TRIVIAL)
    @allure.title("User deletes the file with correct file_id")
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_file(self, private_files_client: PrivateFilesClient, create_file: FileData):
        response = private_files_client.delete_file_api(create_file.response.file.id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_get_file = private_files_client.get_file_api(create_file.response.file.id)
        response_get_file_json = InternalErrorResponseSchema.model_validate_json(response_get_file.text)

        validate_json_schema(instance=response_get_file_json, schema=InternalErrorResponseSchema)

        assert_status_code(response_get_file.status_code, HTTPStatus.NOT_FOUND)
        assert_file_not_found_response(response_get_file_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("User deletes the file with incorrect file_id")
    @pytest.mark.errors
    @allure.severity(Severity.TRIVIAL)
    def test_delete_file_with_incorrect_data(self, private_files_client: PrivateFilesClient, create_file: FileData):
        response = private_files_client.delete_file_api(file_id="incorrect-file-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_json)
