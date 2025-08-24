from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema, InternalErrorResponseSchema
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_length import assert_length


def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")

def assert_validation_error_response(actual: ValidationErrorResponseSchema, expected: ValidationErrorResponseSchema):
    assert_length(actual.details, expected.details, "details")
    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)

def assert_internal_error_response(actual:InternalErrorResponseSchema, expected:InternalErrorResponseSchema):
    assert_length(actual.details, expected.details, "details")