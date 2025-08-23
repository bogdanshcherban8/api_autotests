from typing import Any


def assert_is_true(actual: Any, name: str):
    assert actual, (
        f'Incorrect value: "{name}"',
        f'Expected true value but got: {actual}'
    )
