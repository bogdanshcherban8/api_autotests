from typing import Any

import allure

from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")
@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    logger.info(f"Check that {name} equals to {expected}")
    assert actual == expected, (f'Incorrect value: "{name}"',
                                f'Expected value: {expected}',
                                f'Actual value: {actual}')
