"""
Main application entry point for the Phase I In-Memory Python Console Todo App.
"""

from src.services.task_manager import TaskManager
from src.cli.console_interface import ConsoleInterface


def main():
    """
    Main function to run the Todo application.
    """
    print("Starting Todo Application...")

    # Initialize the task manager and console interface
    task_manager = TaskManager()
    console_interface = ConsoleInterface(task_manager)

    # Run the console interface
    console_interface.run()


if __name__ == "__main__":
    main()