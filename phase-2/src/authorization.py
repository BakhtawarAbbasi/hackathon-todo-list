"""
Authorization module for Todo Backend API
"""
import logging
from uuid import UUID
from fastapi import HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models.task import Task


# Create logger
logger = logging.getLogger(__name__)


async def check_task_ownership(session: AsyncSession, task_id: UUID, user_id: UUID) -> bool:
    """
    Check if a task belongs to a specific user
    """
    try:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.exec(statement)
        task = result.first()

        return task is not None
    except Exception as e:
        logger.error(f"Error checking task ownership for task {task_id} and user {user_id}: {str(e)}")
        raise


def verify_task_access(task_exists: bool) -> None:
    """
    Verify that a user has access to a task
    """
    if not task_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )


def handle_unauthorized_access():
    """
    Handle unauthorized access attempts
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized access to task"
    )


def log_security_event(event_type: str, user_id: UUID, task_id: UUID = None, details: str = None):
    """
    Log security events for audit trail
    """
    logger.info(f"SECURITY EVENT: {event_type} - User: {user_id}, Task: {task_id}, Details: {details}")