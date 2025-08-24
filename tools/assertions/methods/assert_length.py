from typing import Sized


def assert_length(actual: Sized, expected: Sized, name: str):
    assert len(actual) == len(expected), (
        f'Incorrect object length: "{name}"',
        f'Expected length: {len(expected)}',
        f'Actual length: {len(actual)}'
    )
