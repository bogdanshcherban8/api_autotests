from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorsData:
    type_str = "string_too_short"
    type_uuid = "uuid_parsing"
    type_email = "value_error"
    context_str = {"min_length": 1}
    context_uuid = {"error": "invalid length: expected length 32 for simple format, found 0"}
    context_email = {"reason": "An email address must have an @-sign."}
    message_str = "String should have at least 1 character"
    message_uuid = "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    message_email = "value is not a valid email address: An email address must have an @-sign."


class ValidationErrorSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: str
    input: Any
    context: dict[str, Any] = Field(alias="ctx")
    message: str = Field(alias="msg")
    location: list[str] = Field(alias="loc")


class ValidationErrorResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    details: list[ValidationErrorSchema] = Field(alias="detail")


class InternalErrorResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    details: str = Field(alias="detail")
