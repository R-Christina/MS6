"""Validator module — Urban Hub MS6."""

def validate_positive(value: int) -> bool:
    """Return True if value is strictly positive."""
    if not isinstance(value, int):
        raise TypeError("Expected an integer")
    return value > 0


def validate_non_empty_string(text: str) -> bool:
    """Return True if text is a non-empty string."""
    if not isinstance(text, str):
        raise TypeError("Expected a string")
    return len(text.strip()) > 0