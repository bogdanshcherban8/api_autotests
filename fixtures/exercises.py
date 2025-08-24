import pytest
from pydantic import BaseModel


from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from clients.exercises.private_exercises_client import PrivateExercisesClient, get_private_exercises_client
from fixtures.courses import CourseData
from fixtures.users import UserData


class ExerciseData(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema

@pytest.fixture
def create_exercise(private_exercises_client:PrivateExercisesClient, create_course:CourseData)->ExerciseData:
    request = CreateExerciseRequestSchema(course_id=create_course.response.course.id)
    response = private_exercises_client.create_exercise(request)
    return ExerciseData(request=request, response=response)

@pytest.fixture
def private_exercises_client(create_user: UserData)->PrivateExercisesClient:
    return get_private_exercises_client(create_user.login_user)

@pytest.fixture
def private_exercises_client_manual_create_exercise(create_user:UserData)->PrivateExercisesClient:
    return get_private_exercises_client(create_user.login_user)