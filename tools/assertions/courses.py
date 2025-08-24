from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema, CourseSchema, \
    UpdateCourseResponseSchema, UpdateCourseRequestSchema, GetCoursesResponseSchema
from tools.assertions.files import assert_get_file
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true
from tools.assertions.methods.assert_length import assert_length
from tools.assertions.users import assert_get_user_response, assert_get_user


def assert_create_course_response(request:CreateCourseRequestSchema, response:CreateCourseResponseSchema):
    assert_is_true(response.course.id, "id")
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")
    assert_equal(response.course.preview_file.id, request.preview_file_id, "preview_file_id")
    assert_equal(response.course.created_by_user.id, request.created_by_user_id, "created_by_user_id")

def assert_update_course_response(request:UpdateCourseRequestSchema, response:UpdateCourseResponseSchema):
    if request.title is not None:
        assert_equal(response.course.title, request.title, "title")
    if request.max_score is not None:
        assert_equal(response.course.max_score, request.max_score, "max_score")
    if request.min_score is not None:
        assert_equal(response.course.min_score, request.min_score, "min_score")
    if request.description is not None:
        assert_equal(response.course.description, request.description, "description")
    if request.estimated_time is not None:
        assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")

def assert_get_course(request: CourseSchema, response: CourseSchema):
    assert_equal(response.id, request.id, "id")
    assert_equal(response.title, request.title, "title")
    assert_equal(response.max_score, request.max_score, "max_score")
    assert_equal(response.min_score, request.min_score, "min_score")
    assert_equal(response.description, request.description, "description")
    assert_equal(response.estimated_time, request.estimated_time, "estimated_time")
    assert_get_file(response.preview_file, request.preview_file)
    assert_get_user(response.created_by_user, request.created_by_user)

def assert_get_courses_response(get_courses_response: GetCoursesResponseSchema, create_courses_response:list[CreateCourseResponseSchema]):
    assert_length(get_courses_response.courses, create_courses_response, "courses")
    for index, create_course_response in enumerate(create_courses_response):
        assert_get_course(get_courses_response.courses[index], create_course_response.course)
