"""
Integration tests for the toggle task flow.
"""

from src.services.task_manager import TaskManager


class TestToggleTaskFlow:
    """
    Test class for the toggle task flow integration.
    """

    def test_toggle_task_from_incomplete_to_complete(self):
        """
        Test toggling a task from incomplete to complete.
        """
        # Given: A task manager with an incomplete task
        tm = TaskManager()
        task = tm.add_task("Test Task", "Test Description", completed=False)

        # When: The task status is toggled
        toggled_task = tm.toggle_task_status(task.id)

        # Then: The task becomes complete
        assert toggled_task.completed is True

        # And: The task can be retrieved with updated status
        retrieved_task = tm.get_task(task.id)
        assert retrieved_task.completed is True

    def test_toggle_task_from_complete_to_incomplete(self):
        """
        Test toggling a task from complete to incomplete.
        """
        # Given: A task manager with a complete task
        tm = TaskManager()
        task = tm.add_task("Test Task", "Test Description", completed=True)

        # When: The task status is toggled
        toggled_task = tm.toggle_task_status(task.id)

        # Then: The task becomes incomplete
        assert toggled_task.completed is False

        # And: The task can be retrieved with updated status
        retrieved_task = tm.get_task(task.id)
        assert retrieved_task.completed is False

    def test_toggle_task_multiple_times(self):
        """
        Test toggling a task multiple times.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        task = tm.add_task("Test Task", "Test Description", completed=False)

        # When: The task status is toggled multiple times
        # Original: False -> Toggle 1: True -> Toggle 2: False -> Toggle 3: True
        tm.toggle_task_status(task.id)  # Now True
        tm.toggle_task_status(task.id)  # Now False
        final_task = tm.toggle_task_status(task.id)  # Now True

        # Then: The final status is True (toggled 3 times from initial False)
        assert final_task.completed is True

        # And: The task can be retrieved with final status
        retrieved_task = tm.get_task(task.id)
        assert retrieved_task.completed is True

    def test_toggle_task_preserves_other_attributes(self):
        """
        Test that toggling task status preserves other attributes.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        original_task = tm.add_task("Original Title", "Original Description", completed=False)

        # Store original values before toggle
        original_id = original_task.id
        original_title = original_task.title
        original_description = original_task.description
        original_completed = original_task.completed

        # When: The task status is toggled
        toggled_task = tm.toggle_task_status(original_task.id)

        # Then: Only the completion status changes
        assert toggled_task.id == original_id
        assert toggled_task.title == original_title
        assert toggled_task.description == original_description
        assert toggled_task.completed != original_completed  # Status should be different

    def test_toggle_nonexistent_task(self):
        """
        Test that toggling a non-existent task raises an error.
        """
        # Given: A fresh task manager
        tm = TaskManager()

        # When/Then: Attempting to toggle a non-existent task raises KeyError
        try:
            tm.toggle_task_status(999)
            assert False, "Should have raised KeyError"
        except KeyError:
            pass  # Expected behavior

    def test_toggle_task_in_mixed_list(self):
        """
        Test toggling one task in a list with mixed completion statuses.
        """
        # Given: A task manager with tasks having different completion statuses
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1", completed=False)  # Initially incomplete
        task2 = tm.add_task("Task 2", "Description 2", completed=True)   # Initially complete
        task3 = tm.add_task("Task 3", "Description 3", completed=False)  # Initially incomplete

        # When: Only task1's status is toggled
        tm.toggle_task_status(task1.id)

        # Then: Only task1's status changes
        updated_task1 = tm.get_task(task1.id)
        unchanged_task2 = tm.get_task(task2.id)
        unchanged_task3 = tm.get_task(task3.id)

        assert updated_task1.completed is True   # Was False, now True
        assert unchanged_task2.completed is True  # Remains True
        assert unchanged_task3.completed is False # Remains False

    def test_toggle_task_flow_complete(self):
        """
        Test the complete toggle task flow with verification.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        initial_task = tm.add_task("Initial Task", "Initial Description", completed=False)

        # Store initial state before toggle
        initial_completed_state = initial_task.completed

        # When: The task status is toggled
        toggled_task = tm.toggle_task_status(initial_task.id)

        # Then: The task status has changed
        assert initial_completed_state is False  # Original state before toggle
        assert toggled_task.completed is True    # New state after toggle
        assert toggled_task.id == initial_task.id  # ID should remain the same

        # And: The change is persisted
        retrieved_task = tm.get_task(initial_task.id)
        assert retrieved_task.completed is True

        # And: All tasks can still be retrieved
        all_tasks = tm.get_all_tasks()
        assert len(all_tasks) == 1
        assert retrieved_task in all_tasks

    def test_toggle_task_then_modify_other_attributes(self):
        """
        Test that toggling status doesn't interfere with other operations.
        """
        # Given: A task manager with a task
        tm = TaskManager()
        task = tm.add_task("Original Title", "Original Description", completed=False)

        # When: The task status is toggled and then the title is updated
        tm.toggle_task_status(task.id)  # Now complete
        updated_task = tm.update_task(task.id, title="Updated Title")

        # Then: Both changes are applied
        assert updated_task.completed is True  # From toggle
        assert updated_task.title == "Updated Title"  # From update