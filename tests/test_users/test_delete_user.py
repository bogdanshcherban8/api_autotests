from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from fixtures.users import UserData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.users import assert_user_not_found_response, assert_get_user_with_incorrect_data_response
from tools.json_schema import validate_json_schema

@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@pytest.mark.delete
@pytest.mark.users
@pytest.mark.regression
class TestDeleteUser:
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("User deletes the profile with correct user_id")
    def test_delete_user(self, private_users_client: PrivateUsersClient, create_user: UserData):
        response = private_users_client.delete_user_api(create_user.response.user.id)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_get_user = private_users_client.get_user_by_id_api(create_user.response.user.id)
        response_get_user_json = InternalErrorResponseSchema.model_validate_json(response_get_user.text)

        validate_json_schema(instance=response_get_user_json, schema=InternalErrorResponseSchema)

        assert_status_code(response_get_user.status_code, HTTPStatus.UNAUTHORIZED)
        assert_user_not_found_response(response_get_user_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("User deletes the profile with incorrect user_id")
    @pytest.mark.errors
    def test_delete_user_with_incorrect_data(self, private_users_client: PrivateUsersClient, create_user: UserData):
        response = private_users_client.delete_user_api(user_id="incorrect-user-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_user_with_incorrect_data_response(response_json)
