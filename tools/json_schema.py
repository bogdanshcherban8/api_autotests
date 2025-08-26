from typing import Any

import allure
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from pydantic import BaseModel
from tools.logger import get_logger

logger = get_logger("SCHEMA_ASSERTIONS")
@allure.step("Validate JSON schema")
def validate_json_schema(instance: Any, schema: type[BaseModel]):
    logger.info("Validate JSON schema")
    instance_json = instance.model_dump(mode="json", by_alias=True)
    schema_json = schema.model_json_schema()
    validate(instance=instance_json, schema=schema_json, format_checker=Draft202012Validator.FORMAT_CHECKER)
