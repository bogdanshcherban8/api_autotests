from http import HTTPStatus

import pytest

from clients.courses.courses_schema import UpdateCourseResponseSchema, UpdateCourseRequestSchema
from clients.courses.private_courses_client import PrivateCoursesClient
from clients.errors_schema import ValidationErrorResponseSchema
from fixtures.courses import CourseData
from tools.assertions.courses import assert_update_course_response, assert_update_course_with_incorrect_data_response, \
    assert_get_course_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.update
@pytest.mark.courses
@pytest.mark.regression
class TestUpdateCourse:
    def test_update_course(self, private_courses_client: PrivateCoursesClient, create_course: CourseData):
        request = UpdateCourseRequestSchema(title="New Course!", max_score=None, min_score=None, description=None,
                                            estimated_time=None)
        response = private_courses_client.update_course_api(create_course.response.course.id, request)
        response_json = UpdateCourseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=UpdateCourseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_json)

    @pytest.mark.errors
    class TestUpdateCourseWithIncorrectData:
        @pytest.mark.parametrize("field, incorrect_value, location",
                                 [("title", "", "title"), ("description", "", "description"),
                                  ("estimated_time", "", "estimatedTime")])
        def test_update_course_with_incorrect_data(self, private_courses_client: PrivateCoursesClient,
                                                   create_course: CourseData, field, incorrect_value, location):
            request_data = {"title": "Valid", "description": "Valid", "estimated_time": "Valid"}
            request_data[field] = incorrect_value
            request = UpdateCourseRequestSchema(max_score=None, min_score=None, **request_data)

            response = private_courses_client.update_course_api(create_course.response.course.id, request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_update_course_with_incorrect_data_response(response_json, incorrect_value, location)

        def test_update_course_with_incorrect_id(self, private_courses_client: PrivateCoursesClient):
            request = UpdateCourseRequestSchema(title="New Course!", max_score=None, min_score=None, description=None,
                                                estimated_time=None)
            response = private_courses_client.update_course_api("incorrect-course-id", request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_course_with_incorrect_data_response(response_json)