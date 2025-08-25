from http import HTTPStatus

import pytest

from clients.courses.private_courses_client import PrivateCoursesClient
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from fixtures.courses import CourseData
from tools.assertions.courses import assert_course_not_found_response,\
    assert_get_course_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.delete
@pytest.mark.courses
@pytest.mark.regression
class TestDeleteCourse:
    def test_delete_course(self, private_courses_client: PrivateCoursesClient, create_course: CourseData):
        response = private_courses_client.delete_course_api(create_course.response.course.id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_get_course = private_courses_client.get_course_by_id_api(create_course.response.course.id)
        response_get_course_json = InternalErrorResponseSchema.model_validate_json(response_get_course.text)

        validate_json_schema(instance=response_get_course_json, schema=InternalErrorResponseSchema)
        assert_status_code(response_get_course.status_code, HTTPStatus.NOT_FOUND)
        assert_course_not_found_response(response_get_course_json)

    @pytest.mark.errors
    def test_delete_course_with_invalid_data_response(self, private_courses_client: PrivateCoursesClient,
                                                      create_course: CourseData):
        response = private_courses_client.delete_course_api(course_id="incorrect-course-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_course_with_incorrect_data_response(response_json)
