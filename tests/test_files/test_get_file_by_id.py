from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.files.files_schema import GetFileResponseSchema
from clients.files.private_files_client import PrivateFilesClient
from fixtures.files import FileData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.files import assert_get_file_response, assert_get_file_with_incorrect_file_id_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.FILES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@pytest.mark.get
@pytest.mark.users
@pytest.mark.regression
class TestGetFileById:
    @allure.severity(Severity.TRIVIAL)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("User gets the file with correct file_id")
    def test_get_file_by_id(self, private_files_client: PrivateFilesClient, create_file: FileData):
        response = private_files_client.get_file_api(create_file.response.file.id)
        response_json = GetFileResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetFileResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_file_response(response_json, create_file.response.file)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.TRIVIAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("User gets the file with incorrect file_id")
    @pytest.mark.errors
    def test_get_file_with_incorrect_file_id(self, private_files_client: PrivateFilesClient):
        response = private_files_client.get_file_api(file_id="incorrect-file-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_json)
