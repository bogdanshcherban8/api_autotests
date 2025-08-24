from http import HTTPStatus

import pytest

from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.authentication.public_authentication_client import PublicAuthenticationClient
from fixtures.users import UserData

from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.json_schema import validate_json_schema
@pytest.mark.login
@pytest.mark.authentication
@pytest.mark.regression
class TestLogin:
    def test_login(self, create_user:UserData, public_authentication_client:PublicAuthenticationClient):

        request = LoginRequestSchema(email=create_user.email, password=create_user.password)

        response = public_authentication_client.login_api(request)
        response_json = LoginResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=LoginResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_json)
