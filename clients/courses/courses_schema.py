from pydantic import BaseModel, ConfigDict, HttpUrl, EmailStr, Field
from pydantic.alias_generators import to_camel

from tools.faker import fake


class GetCoursesQuerySchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    user_id: str


class CreateCourseRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    title: str = Field(default_factory=fake.text)
    max_score: int = Field(default_factory=lambda: fake.random_int(50, 100))
    min_score: int = Field(default_factory=lambda: fake.random_int(1, 49))
    description: str = Field(default_factory=fake.sentence)
    estimated_time: str = Field(default_factory=lambda: f"{fake.random_int(1, 4)} weeks")
    preview_file_id: str = Field(default_factory=fake.uuid4)
    created_by_user_id: str = Field(default_factory=fake.uuid4)


class UpdateCourseRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    title: str | None
    max_score: int | None
    min_score: int | None
    description: str | None
    estimated_time: str | None


class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl


class UserSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str


class CourseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str
    title: str
    max_score: int
    min_score: int
    description: str
    preview_file: FileSchema
    estimated_time: str
    created_by_user: UserSchema


class CreateCourseResponseSchema(BaseModel):
    course: CourseSchema


class GetCourseResponseSchema(BaseModel):
    course: CourseSchema


class UpdateCourseResponseSchema(BaseModel):
    course: CourseSchema


class DeleteCourseResponseSchema(BaseModel):
    string: str
