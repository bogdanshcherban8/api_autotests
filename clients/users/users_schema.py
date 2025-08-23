from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel

from tools.faker import fake


class UpdateUserRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    email: EmailStr | None
    last_name: str | None
    first_name: str | None
    middle_name: str | None


class UserSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str


class CreateUserResponseSchema(BaseModel):
    user: UserSchema


class GetUserResponseSchema(BaseModel):
    user: UserSchema


class UpdateUserResponseSchema(BaseModel):
    user: UserSchema


class DeleteUserResponseSchema(BaseModel):
    string: str


class CreateUserRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(default_factory=fake.last_name)
    first_name: str = Field(default_factory=fake.first_name)
    middle_name: str = Field(default_factory=fake.middle_name)
