"""
Validation module for Todo Backend API
"""
from typing import Any
import re
from pydantic import ValidationError


def validate_email(email: str) -> bool:
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    return True, ""


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title
    Returns (is_valid, error_message)
    """
    if not title or len(title.strip()) == 0:
        return False, "Title cannot be empty"

    if len(title) > 255:
        return False, "Title cannot exceed 255 characters"

    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """
    Validate task description
    Returns (is_valid, error_message)
    """
    if description and len(description) > 1000:
        return False, "Description cannot exceed 1000 characters"

    return True, ""


def validate_uuid(uuid_str: str) -> bool:
    """
    Validate UUID format
    """
    import uuid
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string to prevent injection attacks
    """
    if input_str is None:
        return None

    # Remove potentially dangerous characters/sequences
    sanitized = input_str.replace('<script', '').replace('javascript:', '')
    return sanitized.strip()


def validate_and_sanitize_input(value: Any, field_type: str) -> tuple[Any, str]:
    """
    Validate and sanitize input based on field type
    Returns (sanitized_value, error_message)
    """
    if field_type == "email":
        if not validate_email(str(value)):
            return None, "Invalid email format"
        return str(value).lower().strip(), ""

    elif field_type == "password":
        is_valid, error_msg = validate_password(str(value))
        if not is_valid:
            return None, error_msg
        return str(value), ""

    elif field_type == "title":
        is_valid, error_msg = validate_title(str(value))
        if not is_valid:
            return None, error_msg
        return sanitize_input(str(value)), ""

    elif field_type == "description":
        is_valid, error_msg = validate_description(str(value))
        if not is_valid:
            return None, error_msg
        return sanitize_input(str(value)), ""

    elif field_type == "uuid":
        if not validate_uuid(str(value)):
            return None, "Invalid UUID format"
        return str(value), ""

    else:
        return value, ""


def validate_request_payload(payload: dict, required_fields: list = None,
                          optional_fields: list = None) -> tuple[bool, str]:
    """
    Validate request payload structure
    """
    errors = []

    if required_fields:
        for field in required_fields:
            if field not in payload or payload[field] is None:
                errors.append(f"Missing required field: {field}")

    if errors:
        return False, "; ".join(errors)

    return True, ""


def validate_pagination_params(skip: int, limit: int) -> tuple[bool, str]:
    """
    Validate pagination parameters
    """
    if skip < 0:
        return False, "skip parameter must be non-negative"

    if limit <= 0 or limit > 1000:
        return False, "limit parameter must be between 1 and 1000"

    return True, ""


def validate_sort_params(sort_by: str, order: str) -> tuple[bool, str]:
    """
    Validate sorting parameters
    """
    valid_sort_fields = ["created_at", "updated_at", "title"]
    if sort_by not in valid_sort_fields:
        return False, f"sort_by must be one of {valid_sort_fields}"

    if order not in ["asc", "desc"]:
        return False, "order must be 'asc' or 'desc'"

    return True, ""