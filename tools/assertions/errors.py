import allure

from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema, InternalErrorResponseSchema
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_length import assert_length

from tools.logger import get_logger
logger = get_logger("ERRORS_ASSERTIONS")
@allure.step("Check error")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    logger.info("Check error")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")


@allure.step("Check validation error response")
def assert_validation_error_response(actual: ValidationErrorResponseSchema, expected: ValidationErrorResponseSchema):
    logger.info("Check validation error response")
    assert_length(actual.details, expected.details, "details")
    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)

@allure.step("Check internal error response")
def assert_internal_error_response(actual: InternalErrorResponseSchema, expected: InternalErrorResponseSchema):
    logger.info("Check internal error response")
    assert_length(actual.details, expected.details, "details")
