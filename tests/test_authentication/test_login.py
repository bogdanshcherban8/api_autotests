from http import HTTPStatus

import pytest

from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.authentication.public_authentication_client import PublicAuthenticationClient
from clients.errors_schema import ValidationErrorResponseSchema, ErrorsData, InternalErrorResponseSchema

from fixtures.users import UserData

from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.authentication import assert_login_response, assert_login_with_incorrect_data_response, \
    assert_login_with_incorrect_password_response
from tools.json_schema import validate_json_schema


@pytest.mark.authentication
@pytest.mark.regression
@pytest.mark.login
class TestLogin:
    def test_login(self, create_user: UserData, public_authentication_client: PublicAuthenticationClient):
        request = LoginRequestSchema(email=create_user.email, password=create_user.password)

        response = public_authentication_client.login_api(request)
        response_json = LoginResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=LoginResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_json)

    @pytest.mark.errors
    class TestLoginWithIncorrectData:
        @pytest.mark.parametrize("field, invalid_value, location, type_text, context, message",
                                 [("email", "", "email", ErrorsData.type_email, ErrorsData.context_email,
                                   ErrorsData.message_email)])
        def test_login_with_incorrect_email(self, create_user: UserData,
                                           public_authentication_client: PublicAuthenticationClient, field, invalid_value,
                                           location, type_text, context, message):
            request_data = {}
            request_data[field] = invalid_value
            request = LoginRequestSchema(**request_data)

            response = public_authentication_client.login_api(request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)
            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_login_with_incorrect_data_response(response_json, type_text, invalid_value, context, message, location)


        def test_login_with_incorrect_password(self, create_user: UserData,
                                           public_authentication_client: PublicAuthenticationClient):
            request = LoginRequestSchema(password="")

            response = public_authentication_client.login_api(request)
            response_json = InternalErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=InternalErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
            assert_login_with_incorrect_password_response(response_json)
