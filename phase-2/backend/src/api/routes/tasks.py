from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from ...database import get_session  # Import from root src directory
from ...models.task import Task
from ...models.user import User
from ...middleware.jwt import JWTBearer
from ...middleware.user_isolation import require_user_access, check_user_owns_resource

router = APIRouter(prefix="/{user_id}", dependencies=[Depends(JWTBearer())])


@router.get("/tasks", response_model=List[dict])
def get_tasks(user_id: str, request: Request, session: Session = Depends(get_session)):
    """Get all tasks for the specified user"""
    # Get the authenticated user from request state
    authenticated_user_id = str(request.state.user.user_id)

    # Verify that the authenticated user is accessing their own data
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only access your own tasks"
        )

    # Query tasks for the authenticated user only
    statement = select(Task).where(Task.user_id == UUID(user_id))
    tasks = session.exec(statement).all()

    # Convert to dict for response, excluding sensitive data
    return [
        {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "user_id": str(task.user_id)
        }
        for task in tasks
    ]


@router.get("/tasks/{task_id}", response_model=dict)
def get_task(user_id: str, task_id: UUID, request: Request, session: Session = Depends(get_session)):
    """Get a specific task for the specified user"""
    authenticated_user_id = str(request.state.user.user_id)

    # Verify that the authenticated user is accessing their own data
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only access your own tasks"
        )

    # Get the task and verify it belongs to the specified user
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only access your own tasks"
        )

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "user_id": str(task.user_id)
    }


@router.post("/tasks", response_model=dict)
def create_task(user_id: str, task_data: dict, request: Request, session: Session = Depends(get_session)):
    """Create a new task for the specified user"""
    authenticated_user_id = str(request.state.user.user_id)

    # Verify that the authenticated user is creating task for themselves
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only create tasks for yourself"
        )

    # Create task with the specified user's ID
    task = Task(
        title=task_data["title"],
        description=task_data.get("description"),
        completed=task_data.get("completed", False),
        user_id=UUID(user_id)
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "user_id": str(task.user_id)
    }


@router.put("/tasks/{task_id}", response_model=dict)
def update_task(user_id: str, task_id: UUID, task_data: dict, request: Request, session: Session = Depends(get_session)):
    """Update a task for the specified user"""
    authenticated_user_id = str(request.state.user.user_id)

    # Verify that the authenticated user is updating their own task
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only update your own tasks"
        )

    # Get the task and verify it belongs to the specified user
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only update your own tasks"
        )

    # Update task fields
    for field, value in task_data.items():
        if hasattr(task, field) and field not in ["id", "user_id"]:  # Prevent changing ID or user ID
            setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "user_id": str(task.user_id)
    }


@router.delete("/tasks/{task_id}")
def delete_task(user_id: str, task_id: UUID, request: Request, session: Session = Depends(get_session)):
    """Delete a task for the specified user"""
    authenticated_user_id = str(request.state.user.user_id)

    # Verify that the authenticated user is deleting their own task
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only delete your own tasks"
        )

    # Get the task and verify it belongs to the specified user
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only delete your own tasks"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=dict)
def toggle_task_completion(user_id: str, task_id: UUID, request: Request, session: Session = Depends(get_session)):
    """Toggle completion status of a task for the specified user"""
    authenticated_user_id = str(request.state.user.user_id)

    # Verify that the authenticated user is updating their own task
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only update your own tasks"
        )

    # Get the task and verify it belongs to the specified user
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only update your own tasks"
        )

    # Toggle the completion status
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "user_id": str(task.user_id)
    }