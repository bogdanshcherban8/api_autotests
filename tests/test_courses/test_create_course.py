from http import HTTPStatus

import pytest

from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from clients.courses.private_courses_client import PrivateCoursesClient
from fixtures.files import FileData
from fixtures.users import UserData
from tools.assertions.courses import assert_create_course_response

from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema

@pytest.mark.create
@pytest.mark.courses
@pytest.mark.regression
class TestCreateCourse:
    def test_create_course(self, create_file:FileData, create_user:UserData, private_courses_client_manual_create_course:PrivateCoursesClient):
        request = CreateCourseRequestSchema(preview_file_id=create_file.response.file.id, created_by_user_id=create_user.response.user.id)

        response = private_courses_client_manual_create_course.create_course_api(request)
        response_json=CreateCourseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateCourseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request=request, response=response_json)