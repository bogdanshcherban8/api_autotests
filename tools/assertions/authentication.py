import allure

from clients.authentication.authentication_schema import LoginResponseSchema, RefreshResponseSchema, TokenSchema
from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema, InternalErrorResponseSchema
from tools.assertions.errors import assert_validation_error_response, \
    assert_internal_error_response
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true
from tools.logger import get_logger

logger = get_logger("AUTHENTICATION_ASSERTIONS")

@allure.step("Check login response")
def assert_login_response(response: LoginResponseSchema):
    logger.info("Check login response")
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")


@allure.step("Check refresh token")
def assert_refresh_token(request: TokenSchema, response: TokenSchema):
    logger.info("Check refresh token")
    assert_equal(request.token_type, response.token_type, "token_type")
    assert request.access_token != response.access_token, ("Access token was not refreshed")
    assert_equal(request.refresh_token, response.refresh_token, "refresh_token")


@allure.step("Check refresh token response")
def assert_refresh_token_response(refresh_token_response: RefreshResponseSchema,
                                  login_response_schema: LoginResponseSchema):
    logger.info("Check refresh token response")
    assert_refresh_token(refresh_token_response.token, login_response_schema.token)


@allure.step("Check login with incorrect data response")
def assert_login_with_incorrect_data_response(actual: ValidationErrorResponseSchema, type_text, invalid_value, context,
                                              message, location):
    logger.info("Check login with incorrect data response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type=type_text,
                input=invalid_value,
                context=context,
                message=message,
                location=["body", location]
            )
        ]
    )
    assert_validation_error_response(actual, expected)


@allure.step("Check login with incorrect password response")
def assert_login_with_incorrect_password_response(actual: InternalErrorResponseSchema):
    logger.info("Check login with incorrect password response")
    expected = InternalErrorResponseSchema(
        details="Invalid credentials"
    )
    assert_internal_error_response(actual, expected)

@allure.step("Check refresh token with incorrect data response")
def assert_refresh_token_with_incorrect_data_response(actual: InternalErrorResponseSchema):
    logger.info("Check refresh token with incorrect data response")
    expected = InternalErrorResponseSchema(
        details="Invalid or expired refresh token"
    )
    assert_internal_error_response(actual, expected)
