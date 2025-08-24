from httpx import Response

from clients.api_client import APIClient
from clients.builders.private_http_builder import get_private_http_client, AuthenticationSchema
from clients.exercises.exercises_schema import GetExerciseQuerySchema, CreateExerciseRequestSchema, \
    CreateExerciseResponseSchema, UpdateExerciseRequestSchema, \
    GetExercisesResponseSchema, UpdateExerciseResponseSchema, GetExerciseResponseSchema


# Приватные методы, которые требуют авторизацию и работают с эксерсайзами
class PrivateExercisesClient(APIClient):
    def get_exercises_api(self, request: GetExerciseQuerySchema) -> Response:
        return self.get("/api/v1/exercises", params=request.model_dump(by_alias=True))

    def get_exercises(self, request: GetExerciseQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(request)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise_api(self, exercise_id: str) -> Response:
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        return self.post("/api/v1/exercises", json=request.model_dump(by_alias=True))

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request.model_dump(by_alias=True, exclude_none=True))

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        return self.delete(f"/api/v1/exercises/{exercise_id}")



def get_private_exercises_client(user: AuthenticationSchema) -> PrivateExercisesClient:
    return PrivateExercisesClient(client=get_private_http_client(user))
