from clients.authentication.authentication_schema import LoginResponseSchema, RefreshResponseSchema, TokenSchema
from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema, InternalErrorResponseSchema
from tools.assertions.errors import assert_validation_error, assert_validation_error_response, \
    assert_internal_error_response
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true


def assert_login_response(response: LoginResponseSchema):
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")


def assert_refresh_token(request: TokenSchema, response: TokenSchema):
    assert_equal(request.token_type, response.token_type, "token_type")
    assert request.access_token != response.access_token, ("Access token was not refreshed")
    assert_equal(request.refresh_token, response.refresh_token, "refresh_token")


def assert_refresh_token_response(refresh_token_response: RefreshResponseSchema,
                                  login_response_schema: LoginResponseSchema):
    assert_refresh_token(refresh_token_response.token, login_response_schema.token)


def assert_login_with_incorrect_data_response(actual: ValidationErrorResponseSchema, type_text, invalid_value, context,
                                              message, location):
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

def assert_login_with_incorrect_password_response(actual: InternalErrorResponseSchema):
    expected=InternalErrorResponseSchema(
        details="Invalid credentials"
    )
    assert_internal_error_response(actual, expected)

def assert_refresh_token_with_incorrect_data_response(actual: InternalErrorResponseSchema):
    expected=InternalErrorResponseSchema(
        details="Invalid or expired refresh token"
    )
    assert_internal_error_response(actual, expected)