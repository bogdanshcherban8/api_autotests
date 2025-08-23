from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true


def assert_create_courses_response(request:CreateCourseRequestSchema, response:CreateCourseResponseSchema):
    assert_is_true(response.course.id, "id")
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")
    assert_equal(response.course.preview_file.id, request.preview_file_id, "preview_file_id")
    assert_equal(response.course.created_by_user.id, request.created_by_user_id, "created_by_user_id")
