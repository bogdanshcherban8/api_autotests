from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.exercises.exercises_schema import GetExerciseQuerySchema, GetExercisesResponseSchema, \
    GetExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient
from fixtures.courses import CourseData

from fixtures.exercises import ExerciseData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.exercises import assert_get_exercises_response, assert_get_exercise_response, \
    assert_get_exercises_with_incorrect_data_response, assert_get_exercise_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema


@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.EXERCISES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@pytest.mark.get
@pytest.mark.exercises
@pytest.mark.regression
class TestGetExercises:
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(Severity.MINOR)
    @allure.title("User gets exercises with correct course_id")
    def test_get_exercises(self, private_exercises_client: PrivateExercisesClient, create_exercise: ExerciseData,
                           create_course: CourseData):
        course_id = GetExerciseQuerySchema(course_id=create_course.response.course.id)

        response = private_exercises_client.get_exercises_api(course_id)
        response_json = GetExercisesResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetExercisesResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercises_response(response_json, [create_exercise.response])

    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.MINOR)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("User gets the exercise with correct exercise_id")
    def test_get_exercise(self, private_exercises_client: PrivateExercisesClient, create_exercise: ExerciseData):
        response = private_exercises_client.get_exercise_by_id_api(create_exercise.response.exercise.id)
        response_json = GetExerciseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetExerciseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(create_exercise.response.exercise, response_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @pytest.mark.errors
    class TestGetExercisesWithIncorrectData:
        @allure.title("User gets exercises with incorrect course_id")
        @allure.severity(Severity.MINOR)
        def test_get_exercises_with_incorrect_data(self, private_exercises_client: PrivateExercisesClient):
            course_id = GetExerciseQuerySchema(course_id="incorrect-course-id")
            response = private_exercises_client.get_exercises_api(course_id)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_exercises_with_incorrect_data_response(response_json)

        @allure.severity(Severity.MINOR)
        @allure.title("User gets the exercise with incorrect exercise_id")
        def test_get_exercise_with_incorrect_data(self, private_exercises_client: PrivateExercisesClient, ):
            response = private_exercises_client.get_exercise_by_id_api(exercise_id="incorrect-exercise-id")
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_exercise_with_incorrect_data_response(response_json)
