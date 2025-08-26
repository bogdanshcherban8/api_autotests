from typing import Any

import allure

from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")
@allure.step("Check that {name} is true")
def assert_is_true(actual: Any, name: str):
    logger.info(f"Check that {name} is true")
    assert actual, (
        f'Incorrect value: "{name}"',
        f'Expected true value but got: {actual}'
    )
