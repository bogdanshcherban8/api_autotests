def assert_status_code(actual: int, expected: int):
    assert actual == expected, (f'Incorrect response status code.',
                                f'Expected status code: {expected}.',
                                f'Actual status code: {actual}')
