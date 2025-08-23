from typing import Any

from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from pydantic import BaseModel


def validate_json_schema(instance: Any, schema: type[BaseModel]):
    instance_json = instance.model_dump(mode="json", by_alias=True)
    schema_json = schema.model_json_schema()
    validate(instance=instance_json, schema=schema_json, format_checker=Draft202012Validator.FORMAT_CHECKER)
