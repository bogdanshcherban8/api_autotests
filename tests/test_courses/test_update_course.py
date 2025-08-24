from http import HTTPStatus

import pytest

from clients.courses.courses_schema import UpdateCourseResponseSchema, UpdateCourseRequestSchema
from clients.courses.private_courses_client import PrivateCoursesClient
from fixtures.courses import CourseData
from tools.assertions.courses import assert_update_course_response
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
