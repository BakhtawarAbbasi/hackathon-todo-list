"""
Error handling module for Todo Backend API
"""
from typing import Optional
from enum import Enum
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import logging


# Create logger
logger = logging.getLogger(__name__)


class ErrorCode(Enum):
    """
    Error codes for the API
    """
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DUPLICATE_RESOURCE = "DUPLICATE_RESOURCE"


class ErrorResponse:
    """
    Standard error response format
    """
    def __init__(self, code: str, message: str, details: Optional[list] = None):
        self.code = code
        self.message = message
        self.details = details or []

    def to_dict(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


def create_error_response(code: ErrorCode, message: str, details: Optional[list] = None):
    """
    Create a standardized error response
    """
    error = ErrorResponse(code.value, message, details)
    logger.error(f"{code.value}: {message}")
    return JSONResponse(
        status_code=get_status_code_from_error(code),
        content=error.to_dict()
    )


def get_status_code_from_error(error_code: ErrorCode) -> int:
    """
    Map error code to HTTP status code
    """
    mapping = {
        ErrorCode.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ErrorCode.RESOURCE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.UNAUTHORIZED_ACCESS: status.HTTP_403_FORBIDDEN,
        ErrorCode.DATABASE_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ErrorCode.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ErrorCode.DUPLICATE_RESOURCE: status.HTTP_409_CONFLICT,
    }
    return mapping.get(error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


async def handle_validation_error(exc: Exception):
    """
    Handle validation errors
    """
    logger.error(f"Validation error: {str(exc)}")
    return create_error_response(
        ErrorCode.VALIDATION_ERROR,
        f"Validation failed: {str(exc)}"
    )


async def handle_database_error(exc: Exception):
    """
    Handle database errors
    """
    logger.error(f"Database error: {str(exc)}")
    return create_error_response(
        ErrorCode.DATABASE_ERROR,
        "Database operation failed"
    )


async def handle_internal_error(exc: Exception):
    """
    Handle internal server errors
    """
    logger.error(f"Internal error: {str(exc)}")
    return create_error_response(
        ErrorCode.INTERNAL_ERROR,
        "Internal server error occurred"
    )


def log_error(error_type: str, error_message: str, user_id: str = None, request_id: str = None):
    """
    Log errors for monitoring
    """
    logger.error(f"ERROR [{error_type}] - Message: {error_message}, "
                 f"User: {user_id}, Request: {request_id}")


def register_error_handlers(app):
    """
    Register error handlers with the FastAPI app
    """
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        log_error("GENERIC", str(exc), getattr(request.state, 'user_id', None) if hasattr(request, 'state') else None)
        return create_error_response(
            ErrorCode.INTERNAL_ERROR,
            "An unexpected error occurred"
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        log_error("HTTP", str(exc.detail), getattr(request.state, 'user_id', None) if hasattr(request, 'state') else None)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                "HTTP_ERROR",
                exc.detail
            ).to_dict()
        )