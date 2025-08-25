from http import HTTPStatus

import pytest

from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from clients.courses.private_courses_client import PrivateCoursesClient
from clients.errors_schema import ValidationErrorResponseSchema, ErrorsData
from fixtures.files import FileData
from fixtures.users import UserData
from tools.assertions.courses import assert_create_course_response, assert_create_course_with_incorrect_data_response

from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.create
@pytest.mark.courses
@pytest.mark.regression
class TestCreateCourse:
    def test_create_course(self, create_file: FileData, create_user: UserData,
                           private_courses_client_manual_create_course: PrivateCoursesClient):
        request = CreateCourseRequestSchema(preview_file_id=create_file.response.file.id,
                                            created_by_user_id=create_user.response.user.id)

        response = private_courses_client_manual_create_course.create_course_api(request)
        response_json = CreateCourseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateCourseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request=request, response=response_json)

    @pytest.mark.errors
    @pytest.mark.parametrize("field, incorrect_value, location, type_text, context, message",
                             [("title", "", "title", ErrorsData.type_str, ErrorsData.context_str,
                               ErrorsData.message_str),
                              ("description", "", "description", ErrorsData.type_str, ErrorsData.context_str,
                               ErrorsData.message_str),
                              ("estimated_time", "", "estimatedTime", ErrorsData.type_str, ErrorsData.context_str,
                               ErrorsData.message_str),
                              ("preview_file_id", "", "previewFileId", ErrorsData.type_uuid, ErrorsData.context_uuid,
                               ErrorsData.message_uuid), ("created_by_user_id", "", "createdByUserId", ErrorsData.type_uuid, ErrorsData.context_uuid,
                               ErrorsData.message_uuid)])
    def test_create_course_with_incorrect_data(self, create_file: FileData, create_user: UserData,
                                               private_courses_client_manual_create_course: PrivateCoursesClient, field,
                                               incorrect_value, location, type_text, context, message):
        request_data = {}
        request_data[field] = incorrect_value
        request = CreateCourseRequestSchema(**request_data)

        response = private_courses_client_manual_create_course.create_course_api(request)
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_course_with_incorrect_data_response(response_json, incorrect_value, location, type_text, context,
                                                          message)
