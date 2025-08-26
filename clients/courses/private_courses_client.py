import allure
from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema, GetCourseQuerySchema, \
    UpdateCourseRequestSchema, GetCourseResponseSchema, UpdateCourseResponseSchema, GetCoursesResponseSchema
from tools.routes import APIRoutes


# Приватные методы, которые требуют авторизацию и работают с курсами
class PrivateCoursesClient(APIClient):
    @allure.step("Create course")
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        return self.post(APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)

    @allure.step("Get courses")
    def get_courses_api(self, request: GetCourseQuerySchema) -> Response:
        return self.get(APIRoutes.COURSES, params=request.model_dump(by_alias=True))

    def get_courses(self, request: GetCourseQuerySchema) -> GetCoursesResponseSchema:
        response = self.get_courses_api(request)
        return GetCoursesResponseSchema.model_validate_json(response.text)

    @allure.step("Get course by id {course_id}")
    def get_course_by_id_api(self, course_id: str) -> Response:
        return self.get(f"{APIRoutes.COURSES}/{course_id}")

    def get_course_by_id(self, course_id: str) -> GetCourseResponseSchema:
        response = self.get_course_by_id_api(course_id)
        return GetCourseResponseSchema.model_validate_json(response.text)

    @allure.step("Update course by id {course_id}")
    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        return self.patch(f"{APIRoutes.COURSES}/{course_id}", json=request.model_dump(by_alias=True, exclude_none=True))

    def update_course(self, course_id: str, request: UpdateCourseRequestSchema) -> UpdateCourseResponseSchema:
        response = self.update_course_api(course_id, request)
        return UpdateCourseResponseSchema.model_validate_json(response.text)

    @allure.step("Delete course by id {course_id}")
    def delete_course_api(self, course_id: str) -> Response:
        return self.delete(f"{APIRoutes.COURSES}/{course_id}")


def get_private_courses_client(user: AuthenticationSchema) -> PrivateCoursesClient:
    return PrivateCoursesClient(client=get_private_http_client(user))
