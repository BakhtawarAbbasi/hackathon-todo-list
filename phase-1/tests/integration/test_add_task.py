"""
Integration tests for the add task flow.
"""

from src.services.task_manager import TaskManager
from src.models.task import Task


class TestAddTaskFlow:
    """
    Test class for the add task flow integration.
    """

    def test_add_task_flow_complete(self):
        """
        Test the complete add task flow from creation to retrieval.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When: A task is added
        new_task = tm.add_task("Buy groceries", "Milk, bread, eggs")

        # Then: The task is created with correct properties
        assert isinstance(new_task, Task)
        assert new_task.id == 1
        assert new_task.title == "Buy groceries"
        assert new_task.description == "Milk, bread, eggs"
        assert new_task.completed is False

        # And: The task can be retrieved
        retrieved_task = tm.get_task(new_task.id)
        assert retrieved_task.id == new_task.id
        assert retrieved_task.title == new_task.title
        assert retrieved_task.description == new_task.description
        assert retrieved_task.completed == new_task.completed

        # And: The task appears in the all tasks list
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 1
        assert new_task in all_tasks

    def test_multiple_add_task_flow(self):
        """
        Test adding multiple tasks and verifying they all exist.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When: Multiple tasks are added
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")
        task3 = tm.add_task("Task 3", "Description 3")

        # Then: All tasks are created with unique IDs
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

        # And: All tasks can be retrieved individually
        retrieved_task1 = tm.get_task(task1.id)
        retrieved_task2 = tm.get_task(task2.id)
        retrieved_task3 = tm.get_task(task3.id)

        assert retrieved_task1.title == "Task 1"
        assert retrieved_task2.title == "Task 2"
        assert retrieved_task3.title == "Task 3"

        # And: All tasks appear in the all tasks list
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks

    def test_add_task_with_empty_description(self):
        """
        Test adding a task with empty description.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When: A task is added with empty description
        new_task = tm.add_task("Task with no description")

        # Then: The task is created with empty description
        assert new_task.id == 1
        assert new_task.title == "Task with no description"
        assert new_task.description == ""
        assert new_task.completed is False

    def test_add_task_with_special_characters(self):
        """
        Test adding a task with special characters in title and description.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When: A task is added with special characters
        special_title = "Task with special chars: !@#$%^&*()"
        special_desc = "Description with special chars: <>{}[]|\\`~"
        new_task = tm.add_task(special_title, special_desc)

        # Then: The task is created with the special characters preserved
        assert new_task.id == 1
        assert new_task.title == special_title
        assert new_task.description == special_desc
        assert new_task.completed is False