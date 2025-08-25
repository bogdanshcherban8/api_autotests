from http import HTTPStatus

import pytest

from clients.authentication.authentication_schema import LoginRequestSchema
from clients.authentication.public_authentication_client import PublicAuthenticationClient
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from fixtures.users import UserData
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.users import assert_user_not_found_response, assert_get_user_with_incorrect_data_response
from tools.json_schema import validate_json_schema


@pytest.mark.delete
@pytest.mark.users
@pytest.mark.regression
class TestDeleteUser:
    def test_delete_user(self, private_users_client:PrivateUsersClient, create_user:UserData):
        response = private_users_client.delete_user_api(create_user.response.user.id)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_get_user=private_users_client.get_user_by_id_api(create_user.response.user.id)
        response_get_user_json= InternalErrorResponseSchema.model_validate_json(response_get_user.text)

        validate_json_schema(instance=response_get_user_json, schema=InternalErrorResponseSchema)

        assert_status_code(response_get_user.status_code, HTTPStatus.UNAUTHORIZED)
        assert_user_not_found_response(response_get_user_json)

    @pytest.mark.errors
    def test_delete_user_with_incorrect_data(self, private_users_client:PrivateUsersClient, create_user:UserData):
        response = private_users_client.delete_user_api(user_id="incorrect-user-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_user_with_incorrect_data_response(response_json)
