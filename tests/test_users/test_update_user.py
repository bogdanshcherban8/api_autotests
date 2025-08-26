from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import UpdateUserRequestSchema, UpdateUserResponseSchema
from fixtures.users import UserData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.users import assert_update_user_response, \
    assert_create_user_with_incorrect_data_response, assert_get_user_with_incorrect_data_response
from tools.json_schema import validate_json_schema
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@pytest.mark.update
@pytest.mark.users
@pytest.mark.regression
class TestUpdateUser:
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("User updates the profile with correct user_id")
    def test_update_user(self, private_users_client: PrivateUsersClient, create_user: UserData):
        request = UpdateUserRequestSchema(email=None, last_name="Bob", first_name=None, middle_name=None)

        response = private_users_client.update_user_api(create_user.response.user.id, request)
        response_json = UpdateUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=UpdateUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(request, response_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @pytest.mark.errors
    class TestUpdateUserWithIncorrectData:
        @allure.severity(Severity.NORMAL)
        @allure.title("User updates the profile with incorrect data")
        @pytest.mark.parametrize("field, incorrect_value, location",
                                 [("last_name", "", "lastName"), ("first_name", "", "firstName"), ("middle_name", "",
                                  "middleName")])
        def test_update_user_with_incorrect_data(self, private_users_client: PrivateUsersClient, create_user: UserData,
                                                 field, incorrect_value, location):
            request_data = {"email": "v@example.com", "last_name": "v", "first_name": "v", "middle_name": "v"}
            request_data[field] = incorrect_value
            request = UpdateUserRequestSchema(**request_data)

            response = private_users_client.update_user_api(create_user.response.user.id, request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_create_user_with_incorrect_data_response(response_json, incorrect_value, location)

        @allure.title("User updates the profile with incorrect user_id")
        @allure.severity(Severity.NORMAL)
        def test_update_user_with_incorrect_id(self, private_users_client: PrivateUsersClient):
            request = UpdateUserRequestSchema(email=None, last_name="Bob", first_name=None, middle_name=None)

            response = private_users_client.update_user_api("incorrect-user-id", request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_user_with_incorrect_data_response(response_json)