from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.courses.private_courses_client import PrivateCoursesClient
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from fixtures.courses import CourseData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.courses import assert_course_not_found_response, \
    assert_get_course_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema

@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@pytest.mark.delete
@pytest.mark.courses
@pytest.mark.regression
class TestDeleteCourse:
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("User deletes course with correct course_id")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_course(self, private_courses_client: PrivateCoursesClient, create_course: CourseData):
        response = private_courses_client.delete_course_api(create_course.response.course.id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_get_course = private_courses_client.get_course_by_id_api(create_course.response.course.id)
        response_get_course_json = InternalErrorResponseSchema.model_validate_json(response_get_course.text)

        validate_json_schema(instance=response_get_course_json, schema=InternalErrorResponseSchema)
        assert_status_code(response_get_course.status_code, HTTPStatus.NOT_FOUND)
        assert_course_not_found_response(response_get_course_json)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("User deletes course with incorrect course_id")
    @pytest.mark.errors
    def test_delete_course_with_invalid_data_response(self, private_courses_client: PrivateCoursesClient,
                                                      create_course: CourseData):
        response = private_courses_client.delete_course_api(course_id="incorrect-course-id")
        response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_course_with_incorrect_data_response(response_json)
