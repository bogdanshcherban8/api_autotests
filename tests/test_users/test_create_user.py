from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.users import assert_create_user_response, assert_create_user_with_incorrect_data_response
from tools.faker import email_param
from tools.json_schema import validate_json_schema
from tools.assertions.methods.assert_status_code import assert_status_code


@pytest.mark.create
@pytest.mark.users
@pytest.mark.regression
class TestCreateUser:
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com"])
    def test_create_user(self, public_users_client: PublicUsersClient, domain):
        request = CreateUserRequestSchema(email=email_param(domain))

        response = public_users_client.create_user_api(request)
        response_json = CreateUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_json)

    @pytest.mark.errors
    @pytest.mark.parametrize("field, invalid_value, location",
                             [("password", "", "password"), ("last_name", "", "lastName"),
                              ("first_name", "", "firstName"), ("middle_name", "", "middleName")])
    def test_create_user_with_incorrect_data(self, public_users_client: PublicUsersClient, field, invalid_value, location):
        request_data = {}
        request_data[field] = invalid_value
        request = CreateUserRequestSchema(**request_data)

        response = public_users_client.create_user_api(request)
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_user_with_incorrect_data_response(response_json, invalid_value, location)
