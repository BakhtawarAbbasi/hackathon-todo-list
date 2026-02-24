"""
Unit tests for services in Todo Backend API
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from uuid import UUID, uuid4

from src.services import TaskService
from src.models.task import Task
from src.models.schemas import TaskCreate, TaskUpdate


@pytest.mark.asyncio
class TestTaskService:
    """Test cases for TaskService"""

    async def test_create_task_success(self):
        """Test successful task creation"""
        # Arrange
        session_mock = AsyncMock()
        user_id = uuid4()
        task_data = TaskCreate(title="Test Task", description="Test Description")

        # Mock the session behavior
        created_task = Task(
            id=uuid4(),
            title=task_data.title,
            description=task_data.description,
            user_id=user_id
        )
        session_mock.add.return_value = None
        session_mock.commit.return_value = None
        session_mock.refresh.return_value = None

        # Act
        result = await TaskService.create_task(session_mock, user_id, task_data)

        # Assert
        assert result.title == task_data.title
        assert result.description == task_data.description
        assert result.user_id == user_id
        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once()

    async def test_get_task_by_id_found(self):
        """Test getting a task that exists"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()

        mock_task = Task(
            id=task_id,
            title="Test Task",
            user_id=user_id
        )

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = mock_task
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.get_task_by_id(session_mock, task_id, user_id)

        # Assert
        assert result == mock_task
        assert result.id == task_id

    async def test_get_task_by_id_not_found(self):
        """Test getting a task that doesn't exist"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = None
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.get_task_by_id(session_mock, task_id, user_id)

        # Assert
        assert result is None

    async def test_get_tasks_for_user(self):
        """Test getting tasks for a specific user"""
        # Arrange
        session_mock = AsyncMock()
        user_id = uuid4()

        mock_tasks = [
            Task(id=uuid4(), title="Task 1", user_id=user_id),
            Task(id=uuid4(), title="Task 2", user_id=user_id)
        ]

        exec_result_mock = MagicMock()
        exec_result_mock.all.return_value = mock_tasks
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.get_tasks_for_user(session_mock, user_id)

        # Assert
        assert len(result) == 2
        assert result[0].user_id == user_id
        assert result[1].user_id == user_id

    async def test_update_task_success(self):
        """Test successful task update"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()
        task_data = TaskUpdate(title="Updated Title")

        existing_task = Task(
            id=task_id,
            title="Original Title",
            user_id=user_id
        )

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = existing_task
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.update_task(session_mock, task_id, user_id, task_data)

        # Assert
        assert result.title == "Updated Title"
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once()

    async def test_update_task_not_found(self):
        """Test updating a task that doesn't exist"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()
        task_data = TaskUpdate(title="Updated Title")

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = None
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.update_task(session_mock, task_id, user_id, task_data)

        # Assert
        assert result is None

    async def test_delete_task_success(self):
        """Test successful task deletion"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()

        existing_task = Task(
            id=task_id,
            title="Test Task",
            user_id=user_id
        )

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = existing_task
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.delete_task(session_mock, task_id, user_id)

        # Assert
        assert result is True
        assert existing_task.is_deleted is True
        assert existing_task.deleted_at is not None
        session_mock.commit.assert_called_once()

    async def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = None
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.delete_task(session_mock, task_id, user_id)

        # Assert
        assert result is False

    async def test_toggle_task_completion(self):
        """Test toggling task completion status"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()

        existing_task = Task(
            id=task_id,
            title="Test Task",
            user_id=user_id,
            completed=False
        )

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = existing_task
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.toggle_task_completion(session_mock, task_id, user_id)

        # Assert
        assert result is not None
        assert result.completed is True
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once()

    async def test_toggle_task_completion_not_found(self):
        """Test toggling completion of a task that doesn't exist"""
        # Arrange
        session_mock = AsyncMock()
        task_id = uuid4()
        user_id = uuid4()

        exec_result_mock = MagicMock()
        exec_result_mock.first.return_value = None
        session_mock.exec.return_value = exec_result_mock

        # Act
        result = await TaskService.toggle_task_completion(session_mock, task_id, user_id)

        # Assert
        assert result is None