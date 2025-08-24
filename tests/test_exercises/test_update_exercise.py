from http import HTTPStatus

import pytest

from clients.exercises.exercises_schema import UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.exercises import ExerciseData
from tools.assertions.exercises import assert_update_exercise_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@pytest.mark.update
@pytest.mark.exercises
@pytest.mark.regression
class TestUpdateExercise:
    def test_update_exercise(self, private_exercises_client: PrivateExercisesClient, create_exercise: ExerciseData):
        request = UpdateExerciseRequestSchema(title="New Course!", max_score=None, min_score=None, order_index=None,
                                              description=None,
                                              estimated_time=None)
        response = private_exercises_client.update_exercise_api(create_exercise.response.exercise.id, request)
        response_json = UpdateExerciseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=UpdateExerciseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_json)
