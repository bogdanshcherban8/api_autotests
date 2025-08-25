from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import GetUserResponseSchema
from fixtures.users import UserData
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.assertions.users import assert_get_user_response, assert_get_user_with_incorrect_data_response
from tools.json_schema import validate_json_schema


@pytest.mark.get
@pytest.mark.users
@pytest.mark.regression
class TestGetUserMe:
    def test_get_user_me(self, private_users_client: PrivateUsersClient, create_user: UserData):
        response = private_users_client.get_user_me_api()
        response_json = GetUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_json, create_user.response.user)

    def test_get_user_by_id(self, private_users_client: PrivateUsersClient, create_user: UserData):
        response = private_users_client.get_user_by_id_api(create_user.response.user.id)
        response_json = GetUserResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetUserResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_json, create_user.response.user)
    @pytest.mark.errors
    class TestGetUserWithIncorrectData:
        def test_get_user_by_id_with_incorrect_data(self, private_users_client: PrivateUsersClient):
            response = private_users_client.get_user_by_id_api(user_id="incorrect-user-id")
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_user_with_incorrect_data_response(response_json)
