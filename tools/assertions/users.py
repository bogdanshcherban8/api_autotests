from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.methods.assert_equal import assert_equal
from clients.users.users_schema import GetUserResponseSchema, UserSchema
from tools.assertions.methods.assert_is_true import assert_is_true


def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")
    assert_is_true(response.user.id, "id")

def assert_get_user(request: UserSchema, response:UserSchema):
    assert_equal(response.id, request.id, "id")
    assert_equal(response.email, request.email, "email")
    assert_equal(response.last_name, request.last_name, "last_name")
    assert_equal(response.first_name, request.first_name, "first_name")
    assert_equal(response.middle_name, request.middle_name, "middle_name")

def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: UserSchema):
    assert_get_user(get_user_response.user, create_user_response)
