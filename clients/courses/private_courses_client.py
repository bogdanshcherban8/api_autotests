from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema, GetCourseQuerySchema, \
    UpdateCourseRequestSchema, GetCourseResponseSchema, UpdateCourseResponseSchema, GetCoursesResponseSchema


# Приватные методы, которые требуют авторизацию и работают с курсами
class PrivateCoursesClient(APIClient):
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        return self.post("/api/v1/courses", json=request.model_dump(by_alias=True))

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)

    def get_courses_api(self, request: GetCourseQuerySchema) -> Response:
        return self.get("/api/v1/courses", params=request.model_dump(by_alias=True))

    def get_courses(self, request: GetCourseQuerySchema) -> GetCoursesResponseSchema:
        response = self.get_courses_api(request)
        return GetCoursesResponseSchema.model_validate_json(response.text)

    def get_course_api(self, course_id: str) -> Response:
        return self.get(f"/api/v1/courses/{course_id}")

    def get_course(self, course_id: str) -> GetCourseResponseSchema:
        response = self.get_course_api(course_id)
        return GetCourseResponseSchema.model_validate_json(response.text)

    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        return self.patch(f"/api/v1/courses/{course_id}", json=request.model_dump(by_alias=True, exclude_none=True))

    def update_course(self, course_id: str, request: UpdateCourseRequestSchema) -> UpdateCourseResponseSchema:
        response = self.update_course_api(course_id, request)
        return UpdateCourseResponseSchema.model_validate_json(response.text)

    def delete_course_api(self, course_id: str) -> Response:
        return self.delete(f"/api/v1/courses/{course_id}")


def get_private_courses_client(user: AuthenticationSchema) -> PrivateCoursesClient:
    return PrivateCoursesClient(client=get_private_http_client(user))
