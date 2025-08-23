from typing import Any


def assert_equal(actual: Any, expected: Any, name: str):
    assert actual == expected, (f'Incorrect value: "{name}"',
                                f'Expected value: {expected}',
                                f'Actual value: {actual}')
