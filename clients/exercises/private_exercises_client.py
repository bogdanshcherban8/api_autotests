from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryDict(TypedDict):
    course_id: str


class CreateExercisesRequestDict(TypedDict):
    title: str
    course_id: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class UpdateExercisesRequestDict(TypedDict):
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None


class ExercisesClient(APIClient):
    def get_exercises_api(self, request: GetExercisesQueryDict) -> Response:
        return self.get("/api/v1/exercises", params=request)

    def get_exercise_api(self, exercise_id: str) -> Response:
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExercisesRequestDict) -> Response:
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, request: UpdateExercisesRequestDict, exercise_id: str)->Response:
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id:str)->Response:
        return self.delete(f"/api/v1/exercises/{exercise_id}")