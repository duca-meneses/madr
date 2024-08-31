import string


def sanitize_data(data: str) -> str:
    sanitized = ''.join(
        char
        if char.isalnum() or char.isspace() or char in string.punctuation
        else ''
        for char in data
    )
    return ' '.join(sanitized.split()).lower()
