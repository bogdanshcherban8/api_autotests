import pytest
from pydantic import BaseModel

from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from clients.courses.private_courses_client import PrivateCoursesClient, get_private_courses_client
from fixtures.files import FileData
from fixtures.users import UserData



class CourseData(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema

@pytest.fixture
def create_course(private_courses_client:PrivateCoursesClient, create_file:FileData, create_user:UserData)->CourseData:
    request=CreateCourseRequestSchema(preview_file_id=create_file.response.file.id, created_by_user_id=create_user.response.user.id)
    response=private_courses_client.create_course(request)
    return CourseData(request=request, response=response)

@pytest.fixture
def private_courses_client(create_user:UserData)->PrivateCoursesClient:
    return get_private_courses_client(create_user.login_user)

@pytest.fixture
def private_courses_client_manual_create_course(create_user:UserData)->PrivateCoursesClient:
    return get_private_courses_client(create_user.login_user)