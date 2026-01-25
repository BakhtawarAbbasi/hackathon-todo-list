"""
ConsoleInterface for managing user interaction through menu or command-driven interface.
"""

from typing import Optional
from src.services.task_manager import TaskManager


class ConsoleInterface:
    """
    Manages user interaction through menu or command-driven interface.
    """

    def __init__(self, task_manager: TaskManager):
        """
        Initialize a new ConsoleInterface instance

        Args:
            task_manager: Instance of TaskManager to interact with
        """
        self.task_manager = task_manager

    def display_menu(self) -> None:
        """
        Display the main menu options to the console
        """
        print("\n" + "="*40)
        print("         TODO APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Status")
        print("6. Exit")
        print("-"*40)

    def get_user_choice(self) -> str:
        """
        Get user's menu choice

        Returns:
            str: The user's choice
        """
        return input("Choose an option (1-6): ").strip()

    def add_task_prompt(self) -> None:
        """
        Prompt user for task details and add to manager
        """
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title cannot be empty.")
                return

            description = input("Enter task description (optional): ").strip()

            task = self.task_manager.add_task(title, description)
            print(f"Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_tasks_prompt(self) -> None:
        """
        Display all tasks to the console
        """
        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("\nNo tasks found.")
            return

        print("\n" + "-"*60)
        print("TASK LIST")
        print("-"*60)
        for task in tasks:
            status = "✓ COMPLETE" if task.completed else "○ INCOMPLETE"
            print(f"ID: {task.id:2d} | {status} | Title: {task.title}")
            if task.description:
                print(f"         Description: {task.description}")
            print("-" * 60)

    def update_task_prompt(self) -> None:
        """
        Prompt user for task ID and new details, then update
        """
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        try:
            task = self.task_manager.get_task(task_id)
            print(f"Current task: {task.title}")

            new_title = input(f"Enter new title (current: '{task.title}'): ").strip()
            if not new_title:
                new_title = None  # Use None to indicate no change

            new_description = input(f"Enter new description (current: '{task.description}'): ").strip()
            if new_description == task.description:
                new_description = None  # Use None to indicate no change

            updated_task = self.task_manager.update_task(
                task_id,
                title=new_title if new_title != task.title else None,
                description=new_description if new_description != task.description else None
            )
            print(f"Task updated successfully.")
        except KeyError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_task_prompt(self) -> None:
        """
        Prompt user for task ID and delete the task
        """
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        try:
            success = self.task_manager.delete_task(task_id)
            if success:
                print(f"Task with ID {task_id} deleted successfully.")
            else:
                print(f"Task with ID {task_id} does not exist.")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def toggle_task_prompt(self) -> None:
        """
        Prompt user for task ID and toggle completion status
        """
        try:
            task_id = int(input("Enter task ID to toggle status: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        try:
            task = self.task_manager.toggle_task_status(task_id)
            status = "completed" if task.completed else "incomplete"
            print(f"Task status updated to {status}.")
        except KeyError as e:
            print(f"Error: {e}")

    def run(self) -> None:
        """
        Main loop to handle user input and execute corresponding actions
        """
        print("Welcome to the Todo App!")
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task_prompt()
            elif choice == "2":
                self.view_tasks_prompt()
            elif choice == "3":
                self.update_task_prompt()
            elif choice == "4":
                self.delete_task_prompt()
            elif choice == "5":
                self.toggle_task_prompt()
            elif choice == "6":
                print("Thank you for using the Todo App. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1-6.")

            input("\nPress Enter to continue...")