from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true


def assert_create_file_response(request:CreateFileRequestSchema, response:CreateFileResponseSchema):
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")
    assert_is_true(response.file.id, "id")
    assert_is_true(response.file.url, "url")