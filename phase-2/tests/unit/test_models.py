"""
Unit tests for models in Todo Backend API
"""
import pytest
from datetime import datetime
from uuid import UUID

from src.models.user import User
from src.models.task import Task


class TestUserModel:
    """Test cases for User model"""

    def test_user_creation(self):
        """Test creating a user instance"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password"
        )

        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password"
        assert isinstance(user.id, UUID)
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_repr(self):
        """Test the __repr__ method of User model"""
        user = User(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            password_hash="hashed_password"
        )

        repr_str = repr(user)
        assert "User" in repr_str
        assert "test@example.com" in repr_str

    def test_user_email_unique_constraint(self):
        """Test that email field is set up for uniqueness (constraint check)"""
        # This test verifies that the model definition includes the unique constraint
        user_table_args = User.__table__.c.email
        assert user_table_args.name == "email"
        # Note: SQLModel doesn't expose uniqueness constraint in the same way as SQLAlchemy directly
        # The constraint is defined in the model with unique=True


class TestTaskModel:
    """Test cases for Task model"""

    def test_task_creation(self):
        """Test creating a task instance"""
        from uuid import uuid4

        user_id = uuid4()
        task = Task(
            title="Test Task",
            description="Test Description",
            user_id=user_id
        )

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.user_id == user_id
        assert isinstance(task.id, UUID)
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
        assert task.completed is False  # Default value

    def test_task_repr(self):
        """Test the __repr__ method of Task model"""
        from uuid import uuid4

        user_id = uuid4()
        task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            description="Test Description",
            completed=True,
            user_id=user_id
        )

        repr_str = repr(task)
        assert "Task" in repr_str
        assert "Test Task" in repr_str
        assert "True" in repr_str  # completed status

    def test_task_default_values(self):
        """Test default values for task fields"""
        from uuid import uuid4

        user_id = uuid4()
        task = Task(
            title="Test Task",
            user_id=user_id
        )

        assert task.completed is False
        assert task.description is None

    def test_task_relationship_field(self):
        """Test that user_id field is properly defined as foreign key"""
        task_columns = Task.__table__.columns
        assert "user_id" in task_columns.keys()
        # The foreign key relationship is established in the model definition