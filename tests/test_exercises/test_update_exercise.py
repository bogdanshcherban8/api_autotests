from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.exercises.exercises_schema import UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.exercises import ExerciseData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.exercises import assert_update_exercise_response, \
    assert_update_exercise_with_incorrect_data_response, assert_get_exercise_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.faker import fake
from tools.json_schema import validate_json_schema


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.EXERCISES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@pytest.mark.update
@pytest.mark.exercises
@pytest.mark.regression
class TestUpdateExercise:
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.MINOR)
    @allure.title("User updates the exercise with correct exercise_id")
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_update_exercise(self, private_exercises_client: PrivateExercisesClient, create_exercise: ExerciseData):
        request = UpdateExerciseRequestSchema(title=fake.text(), max_score=None, min_score=None, order_index=None,
                                              description=None,
                                              estimated_time=None)
        response = private_exercises_client.update_exercise_api(create_exercise.response.exercise.id, request)
        response_json = UpdateExerciseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=UpdateExerciseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @pytest.mark.errors
    class TestUpdateExerciseWithIncorrectData:
        @allure.severity(Severity.MINOR)
        @allure.title("User updates the exercise with incorrect data")
        @pytest.mark.parametrize("field, incorrect_value, location",
                                 [("title", "", "title"), ("description", "", "description"),
                                  ("estimated_time", "", "estimatedTime")])
        def test_update_exercise_with_incorrect_data(self, private_exercises_client: PrivateExercisesClient,
                                                     create_exercise: ExerciseData, field, incorrect_value, location):
            request_data = {"title": "V", "description": "v", "estimated_time": "v"}
            request_data[field] = incorrect_value
            request = UpdateExerciseRequestSchema(max_score=None, min_score=None, order_index=None,
                                                  **request_data)
            response = private_exercises_client.update_exercise_api(create_exercise.response.exercise.id, request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_update_exercise_with_incorrect_data_response(response_json, incorrect_value, location)

        @allure.title("User updates the exercise with incorrect exercise_id")
        @allure.severity(Severity.MINOR)
        def test_update_exercise_with_incorrect_id(self, private_exercises_client: PrivateExercisesClient):
            request = UpdateExerciseRequestSchema(title="New Course!", max_score=None, min_score=None, order_index=None,
                                                  description=None,
                                                  estimated_time=None)
            response = private_exercises_client.update_exercise_api("incorrect-exercise-id", request)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_exercise_with_incorrect_data_response(response_json)
