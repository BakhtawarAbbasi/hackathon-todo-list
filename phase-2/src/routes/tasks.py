"""
Task routes for Todo Backend API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ..models.task import Task
from ..models.schemas import TaskCreate
from ..dependencies import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc


router = APIRouter(
    prefix="/api/{user_id}/tasks",
    tags=["tasks"],
    responses={404: {"description": "User or tasks not found"}},
)


@router.get("/", response_model=List[Task])
async def list_tasks(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    order: str = "desc"
):
    """
    Get all tasks for a specific user with pagination and sorting
    """
    try:
        from ..services import TaskService

        # Get non-deleted tasks for the user
        tasks = await TaskService.get_non_deleted_tasks_for_user(
            session, user_id, skip, limit, sort_by, order
        )

        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.post("/", response_model=Task)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Create a new task for a specific user
    """
    try:
        # Create new task instance with user_id
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id
        )

        # Add to session and commit
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.patch("/{task_id}/complete", response_model=Task)
async def toggle_task_completion(
    user_id: UUID,
    task_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task
    """
    try:
        from ..services import TaskService

        # Validate that task exists and belongs to user
        task = await TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        # Toggle completion status
        task.completed = not task.completed
        await session.commit()
        await session.refresh(task)

        return task
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling task completion: {str(e)}"
        )


@router.put("/{task_id}", response_model=Task)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific task for a user
    """
    try:
        from ..services import TaskService

        # Attempt to update the task
        updated_task = await TaskService.update_task(session, task_id, user_id, task_data)

        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific task for a user
    """
    try:
        from ..services import TaskService

        # Attempt to delete the task
        success = await TaskService.delete_task(session, task_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        # Return 204 No Content on success
        return
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )