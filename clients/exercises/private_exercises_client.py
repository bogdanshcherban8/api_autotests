import allure
from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.exercises.exercises_schema import GetExerciseQuerySchema, CreateExerciseRequestSchema, \
    CreateExerciseResponseSchema, UpdateExerciseRequestSchema, \
    GetExercisesResponseSchema, UpdateExerciseResponseSchema, GetExerciseResponseSchema
from tools.routes import APIRoutes


# Приватные методы, которые требуют авторизацию и работают с эксерсайзами
class PrivateExercisesClient(APIClient):
    @allure.step("Get exercises")
    def get_exercises_api(self, request: GetExerciseQuerySchema) -> Response:
        return self.get(APIRoutes.EXERCISES, params=request.model_dump(by_alias=True))

    def get_exercises(self, request: GetExerciseQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(request)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    @allure.step("Get exercise by id {exercise_id}")
    def get_exercise_by_id_api(self, exercise_id: str) -> Response:
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def get_exercise_by_id(self, exercise_id: str) -> GetExerciseResponseSchema:
        response = self.get_exercise_by_id_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Create exercise")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        return self.post(APIRoutes.EXERCISES, json=request.model_dump(by_alias=True))

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Update exercise by id {exercise_id}")
    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        return self.patch(f"{APIRoutes.EXERCISES}/{exercise_id}", json=request.model_dump(by_alias=True, exclude_none=True))

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Delete exercise by id {exercise_id}")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")



def get_private_exercises_client(user: AuthenticationSchema) -> PrivateExercisesClient:
    return PrivateExercisesClient(client=get_private_http_client(user))
