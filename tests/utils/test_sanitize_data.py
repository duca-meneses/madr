from madr.utils.sanitize import sanitize_data


def test_sanitize_data_removes_special_characters():
    input_data = 'Hello, World! 123'
    expected_output = 'hello, world! 123'
    assert sanitize_data(input_data) == expected_output


def test_sanitize_data_handles_multiple_spaces():
    input_data = '   This    is    a    test   '
    expected_output = 'this is a test'
    assert sanitize_data(input_data) == expected_output


def test_sanitize_data_handles_unicode_characters():
    input_data = 'Café ☕️'
    expected_output = 'café'
    assert sanitize_data(input_data) == expected_output


def test_sanitize_data_preserves_punctuation():
    input_data = 'Hello, World! How are you?'
    expected_output = 'hello, world! how are you?'
    assert sanitize_data(input_data) == expected_output
