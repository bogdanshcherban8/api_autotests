from typing import Sized

import allure
from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")

def assert_length(actual: Sized, expected: Sized, name: str):
    step=f"Check that length of {name} equals to {len(expected)}"
    with allure.step(step):
        logger.info(step)
        assert len(actual) == len(expected), (
            f'Incorrect object length: "{name}"',
            f'Expected length: {len(expected)}',
            f'Actual length: {len(actual)}'
        )
