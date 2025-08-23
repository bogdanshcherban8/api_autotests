from clients.authentication.authentication_schema import LoginResponseSchema
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true


def assert_login_response(response:LoginResponseSchema):
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")