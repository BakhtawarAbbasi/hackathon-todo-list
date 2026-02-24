"""
Service layer for Todo Backend API
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
import logging

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc

from .models.task import Task
from .models.schemas import TaskCreate, TaskUpdate


# Create logger
logger = logging.getLogger(__name__)


class TaskService:
    """
    Service class for handling task-related business logic
    """

    @staticmethod
    async def create_task(session: AsyncSession, user_id: UUID, task_data: TaskCreate) -> Task:
        """
        Create a new task for a user
        """
        try:
            # Create new task instance
            task = Task(
                title=task_data.title,
                description=task_data.description,
                user_id=user_id
            )

            # Add to session and commit
            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task created successfully with ID: {task.id}")
            return task
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            await session.rollback()
            raise

    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Get a task by ID for a specific user
        """
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.exec(statement)
            task = result.first()
            return task
        except Exception as e:
            logger.error(f"Error getting task by ID {task_id}: {str(e)}")
            raise

    @staticmethod
    async def get_tasks_for_user(
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        order: str = "desc"
    ) -> List[Task]:
        """
        Get all tasks for a specific user with pagination and sorting
        """
        try:
            statement = (
                select(Task)
                .where(Task.user_id == user_id)
                .offset(skip)
                .limit(limit)
            )

            # Apply ordering
            if sort_by not in ["created_at", "updated_at", "title"]:
                sort_by = "created_at"

            if order == "asc":
                statement = statement.order_by(getattr(Task, sort_by))
            else:
                statement = statement.order_by(desc(getattr(Task, sort_by)))

            results = await session.exec(statement)
            tasks = results.all()

            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks for user {user_id}: {str(e)}")
            raise

    @staticmethod
    async def update_task(session: AsyncSession, task_id: UUID, user_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a task for a specific user
        """
        try:
            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return None

            # Update fields that were provided
            if task_data.title is not None:
                task.title = task_data.title
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.completed is not None:
                task.completed = task_data.completed

            # Update the timestamp
            task.updated_at = datetime.utcnow()

            # Commit changes
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task updated successfully with ID: {task.id}")
            return task
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            await session.rollback()
            raise

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> bool:
        """
        Soft delete a task for a specific user
        """
        try:
            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return False

            # Perform soft delete
            task.is_deleted = True
            task.deleted_at = datetime.utcnow()

            # Commit changes
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task soft deleted successfully with ID: {task.id}")
            return True
        except Exception as e:
            logger.error(f"Error soft deleting task {task_id}: {str(e)}")
            await session.rollback()
            raise

    @staticmethod
    async def hard_delete_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> bool:
        """
        Hard delete a task for a specific user (permanent deletion)
        """
        try:
            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return False

            # Perform hard delete
            await session.delete(task)
            await session.commit()

            logger.info(f"Task hard deleted successfully with ID: {task.id}")
            return True
        except Exception as e:
            logger.error(f"Error hard deleting task {task_id}: {str(e)}")
            await session.rollback()
            raise

    @staticmethod
    async def get_non_deleted_tasks_for_user(
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        order: str = "desc"
    ) -> List[Task]:
        """
        Get all non-deleted tasks for a specific user with pagination and sorting
        """
        try:
            statement = (
                select(Task)
                .where(Task.user_id == user_id, Task.is_deleted == False)
                .offset(skip)
                .limit(limit)
            )

            # Apply ordering
            if sort_by not in ["created_at", "updated_at", "title"]:
                sort_by = "created_at"

            if order == "asc":
                statement = statement.order_by(getattr(Task, sort_by))
            else:
                statement = statement.order_by(desc(getattr(Task, sort_by)))

            results = await session.exec(statement)
            tasks = results.all()

            return tasks
        except Exception as e:
            logger.error(f"Error getting non-deleted tasks for user {user_id}: {str(e)}")
            raise

    @staticmethod
    async def toggle_task_completion(session: AsyncSession, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Toggle the completion status of a task
        """
        try:
            # Get the existing task
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return None

            # Toggle the completion status
            task.completed = not task.completed
            task.updated_at = task.updated_at  # Update timestamp

            # Commit changes
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task completion toggled successfully with ID: {task.id}")
            return task
        except Exception as e:
            logger.error(f"Error toggling task completion {task_id}: {str(e)}")
            await session.rollback()
            raise