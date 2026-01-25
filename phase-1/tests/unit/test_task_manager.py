"""
Unit tests for the TaskManager service.
"""

import pytest
from src.models.task import Task
from src.services.task_manager import TaskManager


class TestTaskManager:
    """
    Test class for TaskManager service.
    """

    def test_task_manager_initialization(self):
        """
        Test that TaskManager initializes with empty tasks and starts with ID 1.
        """
        tm = TaskManager()

        assert len(tm.get_all_tasks()) == 0
        assert tm.get_next_id() == 1

    def test_add_task_success(self):
        """
        Test adding a task successfully.
        """
        tm = TaskManager()
        task = tm.add_task("Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert len(tm.get_all_tasks()) == 1

    def test_add_task_without_description(self):
        """
        Test adding a task without description.
        """
        tm = TaskManager()
        task = tm.add_task("Test Title")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_assigns_unique_ids(self):
        """
        Test that consecutive tasks get unique IDs.
        """
        tm = TaskManager()
        task1 = tm.add_task("Task 1")
        task2 = tm.add_task("Task 2")
        task3 = tm.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_empty_title(self):
        """
        Test that adding a task with empty title raises ValueError.
        """
        tm = TaskManager()

        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            tm.add_task("")

    def test_add_task_whitespace_only_title(self):
        """
        Test that adding a task with whitespace-only title raises ValueError.
        """
        tm = TaskManager()

        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            tm.add_task("   ")

    def test_get_task_success(self):
        """
        Test retrieving an existing task.
        """
        tm = TaskManager()
        original_task = tm.add_task("Test Title")

        retrieved_task = tm.get_task(original_task.id)

        assert retrieved_task.id == original_task.id
        assert retrieved_task.title == original_task.title
        assert retrieved_task.description == original_task.description
        assert retrieved_task.completed == original_task.completed

    def test_get_task_nonexistent(self):
        """
        Test retrieving a non-existent task raises KeyError.
        """
        tm = TaskManager()

        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            tm.get_task(999)

    def test_get_all_tasks_empty(self):
        """
        Test getting all tasks when none exist.
        """
        tm = TaskManager()
        tasks = tm.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_multiple(self):
        """
        Test getting all tasks when multiple exist.
        """
        tm = TaskManager()
        task1 = tm.add_task("Task 1")
        task2 = tm.add_task("Task 2")
        task3 = tm.add_task("Task 3")

        tasks = tm.get_all_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_update_task_title_only(self):
        """
        Test updating only the title of a task.
        """
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        updated_task = tm.update_task(original_task.id, title="New Title")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_update_task_description_only(self):
        """
        Test updating only the description of a task.
        """
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        updated_task = tm.update_task(original_task.id, description="New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "Original Title"  # Should remain unchanged
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_update_task_both_fields(self):
        """
        Test updating both title and description of a task.
        """
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        updated_task = tm.update_task(original_task.id, title="New Title", description="New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_update_task_nonexistent(self):
        """
        Test updating a non-existent task raises KeyError.
        """
        tm = TaskManager()

        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            tm.update_task(999, title="New Title")

    def test_update_task_empty_title(self):
        """
        Test updating a task with empty title raises ValueError.
        """
        tm = TaskManager()
        original_task = tm.add_task("Original Title")

        with pytest.raises(ValueError, match="Title must be provided and non-empty"):
            tm.update_task(original_task.id, title="")

    def test_delete_task_exists(self):
        """
        Test deleting an existing task.
        """
        tm = TaskManager()
        task = tm.add_task("Test Title")

        result = tm.delete_task(task.id)

        assert result is True
        assert len(tm.get_all_tasks()) == 0

        # Verify the task is really gone
        with pytest.raises(KeyError):
            tm.get_task(task.id)

    def test_delete_task_not_exists(self):
        """
        Test deleting a non-existent task returns False.
        """
        tm = TaskManager()

        result = tm.delete_task(999)

        assert result is False

    def test_toggle_task_status(self):
        """
        Test toggling task status from False to True.
        """
        tm = TaskManager()
        task = tm.add_task("Test Title", completed=False)

        toggled_task = tm.toggle_task_status(task.id)

        assert toggled_task.completed is True

    def test_toggle_task_status_from_true_to_false(self):
        """
        Test toggling task status from True to False.
        """
        tm = TaskManager()
        task = tm.add_task("Test Title", completed=True)

        toggled_task = tm.toggle_task_status(task.id)

        assert toggled_task.completed is False

    def test_toggle_task_nonexistent(self):
        """
        Test toggling status of non-existent task raises KeyError.
        """
        tm = TaskManager()

        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            tm.toggle_task_status(999)