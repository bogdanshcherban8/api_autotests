from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from tools.faker import fake


class GetExercisesQuerySchema(BaseModel):
    course_id: str


class CreateExercisesRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    title: str = Field(default_factory=fake.text)
    course_id: str = Field(default_factory=fake.uuid4)
    max_score: int = Field(default_factory=lambda: fake.random_int(25, 50))
    min_score: int = Field(default_factory=lambda: fake.random_int(1, 24))
    order_index: int = Field(default_factory=lambda: fake.random_int(1, 10))
    description: str = Field(default_factory= fake.sentence)
    estimated_time: str = Field(default_factory=lambda: f"{fake.random_int(1, 7)} days")


class UpdateExercisesRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    title: str | None
    max_score: int | None
    min_score: int | None
    order_index: int | None
    description: str | None
    estimated_time: str | None


class ExerciseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str
    title: str
    course_id: str
    max_score: int
    min_score: int
    order_index: int
    description: str
    estimated_time: str


class CreateExercisesResponseSchema(BaseModel):
    exercise: ExerciseSchema


class GetExercisesResponseSchema(BaseModel):
    exercise: ExerciseSchema


class UpdateExercisesResponseSchema(BaseModel):
    exercise: ExerciseSchema


class DeleteExercisesResponseSchema(BaseModel):
    string: str
