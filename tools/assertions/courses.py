import allure

from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema, CourseSchema, \
    UpdateCourseResponseSchema, UpdateCourseRequestSchema, GetCoursesResponseSchema, GetCourseResponseSchema
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from tools.assertions.errors import assert_internal_error_response, assert_validation_error_response
from tools.assertions.files import assert_get_file
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true
from tools.assertions.methods.assert_length import assert_length
from tools.assertions.users import assert_get_user

from tools.logger import get_logger
logger = get_logger("COURSES_ASSERTIONS")

@allure.step("Check create course response")
def assert_create_course_response(request: CreateCourseRequestSchema, response: CreateCourseResponseSchema):
    logger.info("Check create course response")
    assert_is_true(response.course.id, "id")
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")
    assert_equal(response.course.preview_file.id, request.preview_file_id, "preview_file_id")
    assert_equal(response.course.created_by_user.id, request.created_by_user_id, "created_by_user_id")

@allure.step("Check update course response")
def assert_update_course_response(request: UpdateCourseRequestSchema, response: UpdateCourseResponseSchema):
    logger.info("Check update course response")
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

@allure.step("Check update course with incorrect data response")
def assert_update_course_with_incorrect_data_response(actual: ValidationErrorResponseSchema, incorrect_value, location):
    logger.info("Check update course with incorrect data response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input=incorrect_value,
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", location]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check course")
def assert_get_course(request: CourseSchema, response: CourseSchema):
    logger.info("Check course")
    assert_equal(response.id, request.id, "id")
    assert_equal(response.title, request.title, "title")
    assert_equal(response.max_score, request.max_score, "max_score")
    assert_equal(response.min_score, request.min_score, "min_score")
    assert_equal(response.description, request.description, "description")
    assert_equal(response.estimated_time, request.estimated_time, "estimated_time")
    assert_get_file(response.preview_file, request.preview_file)
    assert_get_user(response.created_by_user, request.created_by_user)

@allure.step("Check get courses response")
def assert_get_courses_response(get_courses_response: GetCoursesResponseSchema,
                                create_courses_response: list[CreateCourseResponseSchema]):
    logger.info("Check get course response")
    assert_length(get_courses_response.courses, create_courses_response, "courses")
    for index, create_course_response in enumerate(create_courses_response):
        assert_get_course(get_courses_response.courses[index], create_course_response.course)

@allure.step("Check get course response")
def assert_get_course_response(get_course_response: GetCourseResponseSchema,
                               create_course_response: CreateCourseResponseSchema):
    logger.info("Check get course response")
    assert_get_course(get_course_response.course, create_course_response.course)

@allure.step("Check get courses with incorrect data response")
def assert_get_courses_with_incorrect_data_response(actual: ValidationErrorResponseSchema):
    logger.info("Check get course with incorrect data response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-user-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["query", "userId"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check course not found response")
def assert_course_not_found_response(actual: InternalErrorResponseSchema):
    logger.info("Check course not found response")
    expected = InternalErrorResponseSchema(details="Course not found")
    assert_internal_error_response(actual, expected)

@allure.step("Check get course with incorrect data response")
def assert_get_course_with_incorrect_data_response(actual: ValidationErrorResponseSchema):
    logger.info("Check get course with incorrect data response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-course-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "course_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check create course with incorrect data response")
def assert_create_course_with_incorrect_data_response(actual: ValidationErrorResponseSchema, invalid_value, location,
                                                      type_text, context, message):
    logger.info("Check create course with incorrect data response")
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
