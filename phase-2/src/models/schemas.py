"""
Schema definitions for Todo Backend API
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from uuid import UUID


class TaskCreate(BaseModel):
    """
    Schema for creating a new task
    """
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 255:
            raise ValueError('Title cannot exceed 255 characters')
        return v.strip()

    @validator('description')
    def description_max_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description cannot exceed 1000 characters')
        return v


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        from_attributes = True

    @validator('title')
    def title_max_length(cls, v):
        if v and len(v) > 255:
            raise ValueError('Title cannot exceed 255 characters')
        return v

    @validator('description')
    def description_max_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description cannot exceed 1000 characters')
        return v


class TaskResponse(BaseModel):
    """
    Schema for task response
    """
    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    """
    Schema for list of tasks response
    """
    tasks: list[TaskResponse]
    total: int
    page: int
    limit: int


class UserCreate(BaseModel):
    """
    Schema for creating a new user
    """
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(BaseModel):
    """
    Schema for user response
    """
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True