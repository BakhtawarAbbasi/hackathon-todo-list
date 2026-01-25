"""
Integration tests for the view tasks flow.
"""

from src.services.task_manager import TaskManager


class TestViewTasksFlow:
    """
    Test class for the view tasks flow integration.
    """

    def test_view_tasks_empty_list(self):
        """
        Test viewing tasks when no tasks exist.
        """
        # Given: A fresh task manager with no tasks
        tm = TaskManager()

        # When: Getting all tasks
        all_tasks = tm.get_all_tasks()

        # Then: An empty list is returned
        assert all_tasks == []
        assert len(all_tasks) == 0

    def test_view_tasks_single_task(self):
        """
        Test viewing tasks when one task exists.
        """
        # Given: A task manager with one task
        tm = TaskManager()
        added_task = tm.add_task("Single Task", "Description for single task")

        # When: Getting all tasks
        all_tasks = tm.get_all_tasks()

        # Then: The list contains the single task
        assert len(all_tasks) == 1
        assert added_task in all_tasks
        assert all_tasks[0].id == added_task.id
        assert all_tasks[0].title == added_task.title
        assert all_tasks[0].description == added_task.description
        assert all_tasks[0].completed == added_task.completed

    def test_view_tasks_multiple_tasks(self):
        """
        Test viewing tasks when multiple tasks exist.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")
        task3 = tm.add_task("Task 3", "Description 3")

        # When: Getting all tasks
        all_tasks = tm.get_all_tasks()

        # Then: The list contains all tasks
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks

        # And: Tasks can be retrieved individually
        retrieved_task1 = tm.get_task(task1.id)
        retrieved_task2 = tm.get_task(task2.id)
        retrieved_task3 = tm.get_task(task3.id)

        assert retrieved_task1 in all_tasks
        assert retrieved_task2 in all_tasks
        assert retrieved_task3 in all_tasks

    def test_view_tasks_after_modifications(self):
        """
        Test viewing tasks after various modifications.
        """
        # Given: A task manager with some tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Initial description")
        task2 = tm.add_task("Task 2", "Another description")

        # When: A task is updated
        tm.update_task(task1.id, title="Updated Task 1", description="Updated description")

        # And: A task status is toggled
        tm.toggle_task_status(task2.id)

        # Then: Getting all tasks reflects the changes
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 2

        # Find the updated task
        updated_task = None
        for task in all_tasks:
            if task.id == task1.id:
                updated_task = task
                break

        assert updated_task is not None
        assert updated_task.title == "Updated Task 1"
        assert updated_task.description == "Updated description"

        # Find the toggled task
        toggled_task = None
        for task in all_tasks:
            if task.id == task2.id:
                toggled_task = task
                break

        assert toggled_task is not None
        assert toggled_task.completed is True

    def test_view_tasks_after_deletion(self):
        """
        Test viewing tasks after one is deleted.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")
        task3 = tm.add_task("Task 3", "Description 3")

        # When: One task is deleted
        tm.delete_task(task2.id)

        # Then: Getting all tasks returns only the remaining tasks
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 2

        # Verify deleted task is not in the list
        assert task1 in all_tasks
        assert task2 not in all_tasks  # This should not be in the list anymore
        assert task3 in all_tasks

        # Verify the deleted task can't be retrieved individually
        try:
            tm.get_task(task2.id)
            assert False, "Task should not be retrievable after deletion"
        except KeyError:
            pass  # Expected behavior

    def test_get_task_individual(self):
        """
        Test retrieving individual tasks by ID.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        original_task = tm.add_task("Test Task", "Test Description")

        # When: Retrieving the task by ID
        retrieved_task = tm.get_task(original_task.id)

        # Then: The retrieved task matches the original
        assert retrieved_task.id == original_task.id
        assert retrieved_task.title == original_task.title
        assert retrieved_task.description == original_task.description
        assert retrieved_task.completed == original_task.completed