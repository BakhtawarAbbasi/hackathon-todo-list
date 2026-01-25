"""
TaskManager service for handling the storage, retrieval, and manipulation of tasks in memory.
"""

from typing import List, Optional
from src.models.task import Task


class TaskManager:
    """
    Handles the storage, retrieval, and manipulation of tasks in memory.
    """

    def __init__(self):
        """
        Initialize a new TaskManager instance
        Creates an empty collection for storing tasks
        """
        self._tasks = {}  # Dictionary to store tasks by ID
        self._next_id = 1  # Counter for generating unique IDs

    def add_task(self, title: str, description: str = "", completed: bool = False) -> Task:
        """
        Add a new task to the collection

        Args:
            title: Title of the task (required)
            description: Description of the task (optional)
            completed: Completion status (default: False)

        Returns:
            Task: The newly created Task object with assigned ID

        Raises:
            ValueError: If title is empty or None
        """
        if not title or not title.strip():
            raise ValueError("Title must be provided and non-empty")

        task_id = self._next_id
        self._next_id += 1

        task = Task(id=task_id, title=title, description=description, completed=completed)
        self._tasks[task_id] = task

        return task

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task: The task object

        Raises:
            KeyError: If task with given ID doesn't exist
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        return self._tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection

        Returns:
            list[Task]: List of all Task objects
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Task:
        """
        Update an existing task's title and/or description

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Task: The updated Task object

        Raises:
            KeyError: If task with given ID doesn't exist
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID

        Args:
            task_id: ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task_status(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task

        Args:
            task_id: ID of the task to toggle

        Returns:
            Task: The updated Task object with toggled status

        Raises:
            KeyError: If task with given ID doesn't exist
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]
        task.completed = not task.completed

        return task

    def get_next_id(self) -> int:
        """
        Get the next available ID without incrementing the counter.

        Returns:
            int: The next available ID
        """
        return self._next_id