"""
Unit tests for the Task model.
"""

import pytest
from src.models.task import Task


class TestTask:
    """
    Test class for Task model.
    """

    def test_task_creation_valid(self):
        """
        Test creating a valid task with all attributes.
        """
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_creation_defaults(self):
        """
        Test creating a task with default values.
        """
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_task_creation_completed_true(self):
        """
        Test creating a task with completed=True.
        """
        task = Task(id=1, title="Test Task", completed=True)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.completed is True

    def test_task_invalid_id_negative(self):
        """
        Test creating a task with negative ID raises ValueError.
        """
        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id=-1, title="Test Task")

    def test_task_invalid_id_zero(self):
        """
        Test creating a task with zero ID raises ValueError.
        """
        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id=0, title="Test Task")

    def test_task_invalid_id_non_integer(self):
        """
        Test creating a task with non-integer ID raises ValueError.
        """
        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id="invalid", title="Test Task")

    def test_task_empty_title(self):
        """
        Test creating a task with empty title raises ValueError.
        """
        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            Task(id=1, title="")

    def test_task_whitespace_only_title(self):
        """
        Test creating a task with whitespace-only title raises ValueError.
        """
        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            Task(id=1, title="   ")

    def test_task_set_title_valid(self):
        """
        Test setting a valid title.
        """
        task = Task(id=1, title="Original Title")
        task.title = "New Title"

        assert task.title == "New Title"

    def test_task_set_title_empty(self):
        """
        Test setting an empty title raises ValueError.
        """
        task = Task(id=1, title="Original Title")

        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            task.title = ""

    def test_task_set_title_whitespace_only(self):
        """
        Test setting a whitespace-only title raises ValueError.
        """
        task = Task(id=1, title="Original Title")

        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            task.title = "   "

    def test_task_set_description(self):
        """
        Test setting a description.
        """
        task = Task(id=1, title="Test Task")
        task.description = "New Description"

        assert task.description == "New Description"

    def test_task_set_description_none_becomes_empty(self):
        """
        Test setting a description to None makes it empty string.
        """
        task = Task(id=1, title="Test Task")
        task.description = None

        assert task.description == ""

    def test_task_set_completed(self):
        """
        Test setting completed status.
        """
        task = Task(id=1, title="Test Task")
        task.completed = True

        assert task.completed is True

    def test_task_str_representation(self):
        """
        Test string representation of task.
        """
        task = Task(id=1, title="Test Task", completed=False)
        expected = "[1] Test Task - Incomplete"

        assert str(task) == expected

    def test_task_str_representation_complete(self):
        """
        Test string representation of completed task.
        """
        task = Task(id=1, title="Test Task", completed=True)
        expected = "[1] Test Task - Complete"

        assert str(task) == expected

    def test_task_repr_representation(self):
        """
        Test repr representation of task.
        """
        task = Task(id=1, title="Test Task", description="Desc", completed=True)
        expected = "Task(id=1, title='Test Task', description='Desc', completed=True)"

        assert repr(task) == expected