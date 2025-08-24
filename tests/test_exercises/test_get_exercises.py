from http import HTTPStatus

import pytest


from clients.exercises.exercises_schema import GetExerciseQuerySchema, GetExercisesResponseSchema, \
    GetExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.courses import CourseData

from fixtures.exercises import ExerciseData
from tools.assertions.exercises import assert_get_exercises_response, assert_get_exercise_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema

@pytest.mark.get
@pytest.mark.exercises
@pytest.mark.regression
class TestGetExercises:
    def test_get_exercises(self, private_exercises_client: PrivateExercisesClient, create_exercise:ExerciseData, create_course:CourseData):
        course_id = GetExerciseQuerySchema(course_id=create_course.response.course.id)

        response = private_exercises_client.get_exercises_api(course_id)
        response_json = GetExercisesResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetExercisesResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercises_response(response_json, [create_exercise.response])

    def test_get_exercise(self, private_exercises_client: PrivateExercisesClient, create_exercise:ExerciseData):
        response=private_exercises_client.get_exercise_api(create_exercise.response.exercise.id)
        response_json=GetExerciseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetExerciseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(create_exercise.response.exercise, response_json)