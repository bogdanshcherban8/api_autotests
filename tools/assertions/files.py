from http import HTTPStatus

import httpx

from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema, InternalErrorResponseSchema
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, FileSchema, \
    GetFileResponseSchema
from tools.assertions.errors import assert_validation_error_response, assert_internal_error_response
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true
from tools.assertions.methods.assert_status_code import assert_status_code


def assert_create_file_response(request: CreateFileRequestSchema, response: CreateFileResponseSchema):
    assert_is_true(response.file.id, "id")
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")
    expected_url = (f"http://localhost:8000/static/{request.directory}/{request.filename}")
    assert_equal(str(response.file.url), expected_url, "url")
    url_is_accessible = httpx.get(str(response.file.url))
    assert_status_code(url_is_accessible.status_code, HTTPStatus.OK)


def assert_get_file(request: FileSchema, response: FileSchema):
    assert_equal(response.id, request.id, "id")
    assert_equal(response.filename, request.filename, "filename")
    assert_equal(response.directory, request.directory, "directory")
    assert_equal(response.url, request.url, "url")


def assert_get_file_response(get_file_response: GetFileResponseSchema, create_user_response: FileSchema):
    assert_get_file(get_file_response.file, create_user_response)


def assert_create_file_with_incorrect_data_response(actual: ValidationErrorResponseSchema, invalid_value, location):
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

def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    expected = InternalErrorResponseSchema(details="File not found")
    assert_internal_error_response(actual, expected)

def assert_get_file_with_incorrect_file_id_response(actual: ValidationErrorResponseSchema):
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-file-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "file_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
