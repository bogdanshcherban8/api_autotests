from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema, RefreshRequestSchema, \
    RefreshResponseSchema
from clients.authentication.public_authentication_client import PublicAuthenticationClient
from clients.errors_schema import InternalErrorResponseSchema
from fixtures.authentication import LoginData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.authentication import assert_refresh_token_response, \
    assert_refresh_token_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@pytest.mark.authentication
@pytest.mark.regression
@pytest.mark.refresh_token
class TestRefresh:
    @allure.sub_suite(AllureStory.REFRESH)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Refresh token with correct refresh_token")
    @allure.story(AllureStory.REFRESH)
    def test_refresh(self, public_authentication_client: PublicAuthenticationClient, login_user: LoginData):
        request = LoginRequestSchema(email=login_user.email, password=login_user.password)
        response = public_authentication_client.login_api(request)
        response_login_json = LoginResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.OK)

        request_refresh_token = RefreshRequestSchema(refresh_token=response_login_json.token.refresh_token)
        response_refresh_token = public_authentication_client.refresh_api(request_refresh_token)
        response_refresh_token_json = RefreshResponseSchema.model_validate_json(response_refresh_token.text)

        validate_json_schema(instance=response_refresh_token_json, schema=RefreshResponseSchema)

        assert_status_code(response_refresh_token.status_code, HTTPStatus.OK)
        assert_refresh_token_response(response_refresh_token_json, response_login_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("Refresh token with incorrect refresh_token")
    @pytest.mark.errors
    def test_refresh_with_incorrect_data(self, public_authentication_client: PublicAuthenticationClient,
                                         login_user: LoginData):
        request = RefreshRequestSchema(refresh_token="")
        response = public_authentication_client.refresh_api(request)
        response_json = InternalErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=InternalErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_refresh_token_with_incorrect_data_response(response_json)
