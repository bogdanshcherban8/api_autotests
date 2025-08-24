from http import HTTPStatus

import pytest

from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.courses import CourseData
from tools.assertions.exercises import assert_create_exercise
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema

@pytest.mark.create
@pytest.mark.exercises
@pytest.mark.regression
class TestCreateExercise:
    def test_create_exercise(self, create_course:CourseData, private_exercises_client_manual_create_exercise:PrivateExercisesClient):
        request= CreateExerciseRequestSchema(course_id=create_course.response.course.id)

        response = private_exercises_client_manual_create_exercise.create_exercise_api(request)
        response_json = CreateExerciseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=CreateExerciseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise(request, response_json)
