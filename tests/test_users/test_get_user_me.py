from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import GetUserResponseSchema
from fixtures.users import UserData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.users import assert_get_user_response, assert_get_user_with_incorrect_data_response
from tools.json_schema import validate_json_schema
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@pytest.mark.get
@pytest.mark.users
@pytest.mark.regression
class TestGetUserMe:
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("User gets the profile with authorized token")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_get_user_me(self, private_users_client: PrivateUsersClient, create_user: UserData):
        response = private_users_client.get_user_me_api()
        response_json = GetUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_json, create_user.response.user)

    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("User gets the profile with correct user_id")
    def test_get_user_by_id(self, private_users_client: PrivateUsersClient, create_user: UserData):
        response = private_users_client.get_user_by_id_api(create_user.response.user.id)
        response_json = GetUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_json, create_user.response.user)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @pytest.mark.errors
    class TestGetUserWithIncorrectData:
        @allure.severity(Severity.NORMAL)
        @allure.title("User gets the profile with incorrect user_id")
        def test_get_user_by_id_with_incorrect_data(self, private_users_client: PrivateUsersClient):
            response = private_users_client.get_user_by_id_api(user_id="incorrect-user-id")
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_user_with_incorrect_data_response(response_json)
