import allure

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserRequestSchema, \
    UpdateUserResponseSchema
from tools.assertions.errors import assert_internal_error_response, assert_validation_error_response
from tools.assertions.methods.assert_equal import assert_equal
from clients.users.users_schema import GetUserResponseSchema, UserSchema
from tools.assertions.methods.assert_is_true import assert_is_true

from tools.logger import get_logger
logger = get_logger("USERS_ASSERTIONS")

@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    logger.info("Check create user response")
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")
    assert_is_true(response.user.id, "id")


@allure.step("Check user")
def assert_get_user(request: UserSchema, response: UserSchema):
    logger.info("Check user")
    assert_equal(response.id, request.id, "id")
    assert_equal(response.email, request.email, "email")
    assert_equal(response.last_name, request.last_name, "last_name")
    assert_equal(response.first_name, request.first_name, "first_name")
    assert_equal(response.middle_name, request.middle_name, "middle_name")


@allure.step("Check get user response")
def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: UserSchema):
    logger.info("Check get user response")
    assert_get_user(get_user_response.user, create_user_response)

@allure.step("Check get user with incorrect data response")
def assert_get_user_with_incorrect_data_response(actual: ValidationErrorResponseSchema):
    logger.info("Check get user with incorrect data response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-user-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "user_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check user not found response")
def assert_user_not_found_response(actual: InternalErrorResponseSchema):
    logger.info("Check user not found response")
    expected = InternalErrorResponseSchema(details="Invalid or expired token")
    assert_internal_error_response(actual, expected)

@allure.step("Check update user response")
def assert_update_user_response(request: UpdateUserRequestSchema, response: UpdateUserResponseSchema):
    logger.info("Check update user response")
    if request.email is not None:
        assert_equal(response.user.email, request.email, "email")
    if request.last_name is not None:
        assert_equal(response.user.last_name, request.last_name, "last_name")
    if request.first_name is not None:
        assert_equal(response.user.first_name, request.first_name, "first_name")
    if request.middle_name is not None:
        assert_equal(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Check create user with incorrect data response")
def assert_create_user_with_incorrect_data_response(actual: ValidationErrorResponseSchema, invalid_value, location):
    logger.info("Check create user with incorrect data response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input=invalid_value,
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", location]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
