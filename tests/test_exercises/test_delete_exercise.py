from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.exercises import ExerciseData
from tools.assertions.exercises import assert_exercise_not_found_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.delete
@pytest.mark.exercises
@pytest.mark.regression
class TestDeleteExercise:
    def test_delete_exercise(self, private_exercises_client: PrivateExercisesClient, create_exercise: ExerciseData):
        response = private_exercises_client.delete_exercise_api(create_exercise.response.exercise.id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_get_file = private_exercises_client.get_exercise_api(create_exercise.response.exercise.id)
        response_get_file_json = InternalErrorResponseSchema.model_validate_json(response_get_file.text)

        validate_json_schema(instance=response_get_file_json, schema=InternalErrorResponseSchema)

        assert_status_code(response_get_file.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(response_get_file_json)
