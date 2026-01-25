"""
Integration tests for the update task flow.
"""

from src.services.task_manager import TaskManager


class TestUpdateTaskFlow:
    """
    Test class for the update task flow integration.
    """

    def test_update_task_title_only(self):
        """
        Test updating only the title of a task.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        # When: The task title is updated
        updated_task = tm.update_task(original_task.id, title="New Title")

        # Then: Only the title is changed
        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"
        assert updated_task.completed == original_task.completed

        # And: The task can be retrieved with updated information
        retrieved_task = tm.get_task(original_task.id)
        assert retrieved_task.title == "New Title"
        assert retrieved_task.description == "Original Description"

    def test_update_task_description_only(self):
        """
        Test updating only the description of a task.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        # When: The task description is updated
        updated_task = tm.update_task(original_task.id, description="New Description")

        # Then: Only the description is changed
        assert updated_task.id == original_task.id
        assert updated_task.title == "Original Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed

        # And: The task can be retrieved with updated information
        retrieved_task = tm.get_task(original_task.id)
        assert retrieved_task.title == "Original Title"
        assert retrieved_task.description == "New Description"

    def test_update_task_both_fields(self):
        """
        Test updating both title and description of a task.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        # When: Both title and description are updated
        updated_task = tm.update_task(original_task.id, title="New Title", description="New Description")

        # Then: Both fields are changed
        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed

        # And: The task can be retrieved with updated information
        retrieved_task = tm.get_task(original_task.id)
        assert retrieved_task.title == "New Title"
        assert retrieved_task.description == "New Description"

    def test_update_task_preserves_other_attributes(self):
        """
        Test that updating a task preserves other attributes like completion status.
        """
        # Given: A task manager with a completed task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description", completed=True)

        # When: Only the title is updated
        updated_task = tm.update_task(original_task.id, title="New Title")

        # Then: The completion status is preserved
        assert updated_task.title == "New Title"
        assert updated_task.completed is True

    def test_update_task_with_special_characters(self):
        """
        Test updating a task with special characters in title and description.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        # When: The task is updated with special characters
        special_title = "Updated Title with special chars: !@#$%^&*()"
        special_desc = "Updated Description with special chars: <>{}[]|\\`~"
        updated_task = tm.update_task(original_task.id, title=special_title, description=special_desc)

        # Then: The special characters are preserved
        assert updated_task.title == special_title
        assert updated_task.description == special_desc

    def test_update_nonexistent_task(self):
        """
        Test that updating a non-existent task raises an error.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When/Then: Attempting to update a non-existent task raises KeyError
        try:
            tm.update_task(999, title="New Title")
            assert False, "Should have raised KeyError"
        except KeyError:
            pass  # Expected behavior

    def test_update_task_with_empty_title_fails(self):
        """
        Test that updating a task with empty title raises an error.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description")

        # When/Then: Attempting to update with empty title raises ValueError
        try:
            tm.update_task(original_task.id, title="")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected behavior

        # And: The original task remains unchanged
        unchanged_task = tm.get_task(original_task.id)
        assert unchanged_task.title == "Original Title"
        assert unchanged_task.description == "Original Description"

    def test_update_task_flow_complete(self):
        """
        Test the complete update task flow.
        """
        # Given: A task manager with multiple tasks
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")

        # When: One task is updated
        updated_task = tm.update_task(task1.id, title="Updated Task 1", description="Updated Description 1")

        # Then: The updated task has new values
        assert updated_task.title == "Updated Task 1"
        assert updated_task.description == "Updated Description 1"

        # And: The other task remains unchanged
        other_task = tm.get_task(task2.id)
        assert other_task.title == "Task 2"
        assert other_task.description == "Description 2"

        # And: All tasks can still be retrieved
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 2