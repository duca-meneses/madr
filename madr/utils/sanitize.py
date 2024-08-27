def sanitize_data(data: str) -> str:
    sanitized = ''.join(
        char for char in data if char.isalnum() or char.isspace()
    )
    return ' '.join(sanitized.split()).lower()
