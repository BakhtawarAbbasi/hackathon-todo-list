from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship
from .user import User


class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a specific user"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_deleted: bool = Field(default=False)  # For soft delete functionality
    deleted_at: Optional[datetime] = Field(default=None)  # Timestamp when deleted

    # Foreign key relationship
    user_id: UUID = Field(nullable=False, foreign_key="user.id")

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, completed={self.completed}, user_id={self.user_id})"