import allure
from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")

@allure.step("Check that response status code equals to {expected}")
def assert_status_code(actual: int, expected: int):
    logger.info(f"Check that response status code equals to {expected}")
    assert actual == expected, (f'Incorrect response status code.',
                                f'Expected status code: {expected}.',
                                f'Actual status code: {actual}')
