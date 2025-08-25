from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema, ErrorsData
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.courses import CourseData
from tools.assertions.exercises import assert_create_exercise, assert_create_exercise_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.create
@pytest.mark.exercises
@pytest.mark.regression
class TestCreateExercise:
    def test_create_exercise(self, create_course: CourseData,
                             private_exercises_client_manual_create_exercise: PrivateExercisesClient):
        request = CreateExerciseRequestSchema(course_id=create_course.response.course.id)

        response = private_exercises_client_manual_create_exercise.create_exercise_api(request)
        response_json = CreateExerciseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateExerciseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise(request, response_json)

    @pytest.mark.errors
    @pytest.mark.parametrize("field, incorrect_value, location, type_text, context, message",
                             [("title", "", "title", ErrorsData.type_str, ErrorsData.context_str,
                               ErrorsData.message_str),
                              ("description", "", "description", ErrorsData.type_str, ErrorsData.context_str,
                               ErrorsData.message_str),
                              ("estimated_time", "", "estimatedTime", ErrorsData.type_str, ErrorsData.context_str,
                               ErrorsData.message_str),
                              ("course_id", "", "courseId", ErrorsData.type_uuid, ErrorsData.context_uuid,
                               ErrorsData.message_uuid)])
    def test_create_exercise_with_incorrect_data(self, create_course: CourseData,
                                                 private_exercises_client_manual_create_exercise: PrivateExercisesClient,
                                                 field, incorrect_value, location, type_text, context, message):
        request_data = {}
        request_data[field] = incorrect_value
        request = CreateExerciseRequestSchema(**request_data)

        response = private_exercises_client_manual_create_exercise.create_exercise_api(request)
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_exercise_with_incorrect_data_response(response_json, incorrect_value, location, type_text,
                                                            context, message)
