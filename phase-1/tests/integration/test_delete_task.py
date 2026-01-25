"""
Integration tests for the delete task flow.
"""

from src.services.task_manager import TaskManager


class TestDeleteTaskFlow:
    """
    Test class for the delete task flow integration.
    """

    def test_delete_single_task(self):
        """
        Test deleting a single task from the list.
        """
        # Given: A task manager with one task
        tm = TaskManager()
        task = tm.add_task("Task to Delete", "Description to delete")

        # When: The task is deleted
        result = tm.delete_task(task.id)

        # Then: The deletion is successful
        assert result is True

        # And: The task list is now empty
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 0

        # And: The task can no longer be retrieved
        try:
            tm.get_task(task.id)
            assert False, "Task should not be retrievable after deletion"
        except KeyError:
            pass  # Expected behavior

    def test_delete_task_from_multiple(self):
        """
        Test deleting one task from multiple tasks.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")
        task3 = tm.add_task("Task 3", "Description 3")

        # When: One task is deleted
        result = tm.delete_task(task2.id)

        # Then: The deletion is successful
        assert result is True

        # And: The other tasks remain
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 not in all_tasks  # This should be gone
        assert task3 in all_tasks

        # And: The deleted task can no longer be retrieved
        try:
            tm.get_task(task2.id)
            assert False, "Task should not be retrievable after deletion"
        except KeyError:
            pass  # Expected behavior

        # But other tasks can still be retrieved
        retrieved_task1 = tm.get_task(task1.id)
        retrieved_task3 = tm.get_task(task3.id)
        assert retrieved_task1.title == "Task 1"
        assert retrieved_task3.title == "Task 3"

    def test_delete_nonexistent_task(self):
        """
        Test deleting a non-existent task.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When: Attempting to delete a non-existent task
        result = tm.delete_task(999)

        # Then: The result indicates failure
        assert result is False

        # And: The task list remains empty
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 0

    def test_delete_all_tasks(self):
        """
        Test deleting all tasks one by one.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")
        task3 = tm.add_task("Task 3", "Description 3")

        # When: All tasks are deleted
        result1 = tm.delete_task(task1.id)
        result2 = tm.delete_task(task2.id)
        result3 = tm.delete_task(task3.id)

        # Then: All deletions are successful
        assert result1 is True
        assert result2 is True
        assert result3 is True

        # And: The task list is now empty
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 0

        # And: No tasks can be retrieved
        for task_id in [task1.id, task2.id, task3.id]:
            try:
                tm.get_task(task_id)
                assert False, f"Task {task_id} should not be retrievable after deletion"
            except KeyError:
                pass  # Expected behavior

    def test_delete_task_preserves_id_sequence(self):
        """
        Test that deleting a task doesn't affect ID assignment for new tasks.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")
        task3 = tm.add_task("Task 3", "Description 3")

        # When: The middle task is deleted
        tm.delete_task(task2.id)

        # And: A new task is added
        new_task = tm.add_task("New Task", "New Description")

        # Then: The new task gets the next available ID
        assert new_task.id == 4  # Next ID after 1, 2, 3

        # And: The remaining tasks keep their IDs
        remaining_tasks = tm.get_all_tasks()
        task_ids = [task.id for task in remaining_tasks]
        assert task1.id in task_ids
        assert task2.id not in task_ids  # Deleted task ID not present
        assert task3.id in task_ids
        assert new_task.id in task_ids

    def test_delete_task_flow_complete(self):
        """
        Test the complete delete task flow with verification.
        """
        # Given: A task manager with tasks
        tm = TaskManager()
        initial_task = tm.add_task("Initial Task", "Initial Description")

        # When: The task is deleted
        delete_result = tm.delete_task(initial_task.id)

        # Then: The result confirms deletion
        assert delete_result is True

        # And: The task count decreases
        all_tasks_after = tm.get_all_tasks()
        assert len(all_tasks_after) == 0

        # And: Attempting to retrieve the deleted task raises an error
        retrieval_error_occurred = False
        try:
            tm.get_task(initial_task.id)
        except KeyError:
            retrieval_error_occurred = True

        assert retrieval_error_occurred, "Should raise KeyError when retrieving deleted task"

        # And: Adding a new task works normally
        new_task = tm.add_task("New Task After Deletion", "Description")
        assert new_task.id == 2  # First task got ID 1, was deleted, next gets ID 2