from http import HTTPStatus

import pytest

from clients.courses.courses_schema import GetCoursesResponseSchema, GetCourseQuerySchema
from clients.courses.private_courses_client import PrivateCoursesClient
from fixtures.courses import CourseData
from tools.assertions.courses import assert_get_courses_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.get
@pytest.mark.courses
@pytest.mark.regression
class TestGetCourses:
    def test_get_courses(self, private_courses_client:PrivateCoursesClient, create_course:CourseData):
        user_id = GetCourseQuerySchema(user_id=create_course.response.course.created_by_user.id)
        response = private_courses_client.get_courses_api(user_id)
        response_json = GetCoursesResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetCoursesResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(response_json, [create_course.response])