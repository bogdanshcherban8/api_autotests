from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.courses.courses_schema import GetCoursesResponseSchema, GetCourseQuerySchema, GetCourseResponseSchema
from clients.courses.private_courses_client import PrivateCoursesClient
from clients.errors_schema import ValidationErrorResponseSchema
from fixtures.courses import CourseData
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.assertions.courses import assert_get_courses_response, assert_get_course_response, \
    assert_get_courses_with_incorrect_data_response, assert_get_course_with_incorrect_data_response
from tools.assertions.methods.assert_status_code import assert_status_code
from tools.json_schema import validate_json_schema
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@pytest.mark.get
@pytest.mark.courses
@pytest.mark.regression
class TestGetCourses:
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.title("User gets all courses with correct user_id")
    def test_get_courses(self, private_courses_client: PrivateCoursesClient, create_course: CourseData):
        user_id = GetCourseQuerySchema(user_id=create_course.response.course.created_by_user.id)
        response = private_courses_client.get_courses_api(user_id)
        response_json = GetCoursesResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetCoursesResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(response_json, [create_course.response])

    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("User gets the course with correct course_id")
    def test_get_course(self, private_courses_client: PrivateCoursesClient, create_course: CourseData):
        response = private_courses_client.get_course_by_id_api(create_course.response.course.id)
        response_json = GetCourseResponseSchema.model_validate_json(response.text)

        validate_json_schema(instance=response_json, schema=GetCourseResponseSchema)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_course_response(response_json, create_course.response)

    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @pytest.mark.errors
    class TestGetCourseWithIncorrectData:
        @allure.severity(Severity.NORMAL)
        @allure.title("User gets all courses with incorrect user_id")
        def test_get_courses_with_incorrect_data(self, private_courses_client: PrivateCoursesClient,
                                                 create_course: CourseData):
            user_id = GetCourseQuerySchema(user_id="incorrect-user-id")
            response = private_courses_client.get_courses_api(user_id)
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_courses_with_incorrect_data_response(response_json)

        @allure.severity(Severity.NORMAL)
        @allure.title("User gets the course with incorrect course_id")
        def test_get_course_with_incorrect_data(self, private_courses_client: PrivateCoursesClient,
                                                 create_course: CourseData):

            response = private_courses_client.get_course_by_id_api(course_id="incorrect-course-id")
            response_json = ValidationErrorResponseSchema.model_validate_json(response.text)

            validate_json_schema(instance=response_json, schema=ValidationErrorResponseSchema)

            assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
            assert_get_course_with_incorrect_data_response(response_json)

