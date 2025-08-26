from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.users import assert_create_user_response, assert_create_user_with_incorrect_data_response
from tools.faker import email_param
from tools.json_schema import validate_json_schema
from tools.assertions.methods.assert_status_code import assert_status_code


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@pytest.mark.create
@pytest.mark.users
@pytest.mark.regression
class TestCreateUser:
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.title("User creates the profile with correct data")
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com"])
    def test_create_user(self, public_users_client: PublicUsersClient, domain):
        request = CreateUserRequestSchema(email=email_param(domain))

        response = public_users_client.create_user_api(request)
        response_json = CreateUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("User creates the profile with incorrect data")
    @pytest.mark.errors
    @pytest.mark.parametrize("field, invalid_value, location",
                             [("password", "", "password"), ("last_name", "", "lastName"),
                              ("first_name", "", "firstName"), ("middle_name", "", "middleName")])
    def test_create_user_with_incorrect_data(self, public_users_client: PublicUsersClient, field, invalid_value,
                                             location):
        request_data = {}
        request_data[field] = invalid_value
        request = CreateUserRequestSchema(**request_data)

        response = public_users_client.create_user_api(request)
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_user_with_incorrect_data_response(response_json, invalid_value, location)
