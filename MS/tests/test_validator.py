"""Unit tests for the validator module."""
import pytest
from src.domain.validator import validate_positive, validate_non_empty_string


def test_validate_positive_true():
    assert validate_positive(5) is True


def test_validate_positive_false():
    assert validate_positive(-1) is False


def test_validate_positive_zero():
    assert validate_positive(0) is False


def test_validate_positive_type_error():
    with pytest.raises(TypeError):
        validate_positive("abc")


def test_validate_non_empty_string_true():
    assert validate_non_empty_string("hello") is True


def test_validate_non_empty_string_false():
    assert validate_non_empty_string("   ") is False


def test_validate_non_empty_string_type_error():
    with pytest.raises(TypeError):
        validate_non_empty_string(42)