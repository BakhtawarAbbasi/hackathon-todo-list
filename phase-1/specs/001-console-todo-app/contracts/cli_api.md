# CLI API Contracts: Console Todo App

## Overview
This document defines the interface contracts for the console-based todo application. Since this is a Phase I in-memory console application, the "API" consists of function interfaces within the application modules.

## Task Model Interface

### Task Class
```python
class Task:
    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a new Task instance

        Args:
            id: Unique identifier for the task
            title: Title of the task (required)
            description: Description of the task (optional)
            completed: Completion status (default: False)
        """

    @property
    def id(self) -> int:
        """Get the task ID"""

    @property
    def title(self) -> str:
        """Get the task title"""

    @property
    def description(self) -> str:
        """Get the task description"""

    @property
    def completed(self) -> bool:
        """Get the completion status"""

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title"""

    @description.setter
    def description(self, value: str) -> None:
        """Set the task description"""

    @completed.setter
    def completed(self, value: bool) -> None:
        """Set the completion status"""
```

## Task Manager Interface

### TaskManager Class
```python
class TaskManager:
    def __init__(self):
        """
        Initialize a new TaskManager instance
        Creates an empty collection for storing tasks
        """

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the collection

        Args:
            title: Title of the task (required)
            description: Description of the task (optional)

        Returns:
            Task: The newly created Task object with assigned ID

        Raises:
            ValueError: If title is empty or None
        """

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

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks in the collection

        Returns:
            list[Task]: List of all Task objects
        """

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

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID

        Args:
            task_id: ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task didn't exist
        """

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
```

## Console Interface Interface

### ConsoleInterface Class
```python
class ConsoleInterface:
    def __init__(self, task_manager: TaskManager):
        """
        Initialize a new ConsoleInterface instance

        Args:
            task_manager: Instance of TaskManager to interact with
        """

    def display_menu(self) -> None:
        """
        Display the main menu options to the console
        """

    def handle_user_input(self) -> None:
        """
        Main loop to handle user input and execute corresponding actions
        """

    def add_task_prompt(self) -> None:
        """
        Prompt user for task details and add to manager
        """

    def view_tasks_prompt(self) -> None:
        """
        Display all tasks to the console
        """

    def update_task_prompt(self) -> None:
        """
        Prompt user for task ID and new details, then update
        """

    def delete_task_prompt(self) -> None:
        """
        Prompt user for task ID and delete the task
        """

    def toggle_task_prompt(self) -> None:
        """
        Prompt user for task ID and toggle completion status
        """
```