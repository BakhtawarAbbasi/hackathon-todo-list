# Phase I Console Todo App

A simple, in-memory Python console Todo application that allows users to manage their tasks through a menu-driven interface.

## Features

- Add new tasks with titles and descriptions
- View all tasks with their status
- Update existing task titles and descriptions
- Delete tasks
- Toggle task completion status
- Menu-driven console interface

## Prerequisites

- Python 3.13 or higher

## Setup

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies (if any) with `pip install -e .` (optional, as this project uses only built-in libraries)

## Usage

To run the application:

```bash
python src/main.py
```

The application will present a menu with the following options:
1. Add Task - Add a new task with title and description
2. View Tasks - Display all tasks with their status
3. Update Task - Modify an existing task's title and description
4. Delete Task - Remove a task from the list
5. Toggle Task Status - Mark a task as complete/incomplete
6. Exit - Quit the application

## Project Structure

```
src/
├── models/
│   └── task.py          # Task data model definition
├── services/
│   └── task_manager.py  # In-memory storage and business logic
├── cli/
│   └── console_interface.py  # Menu-driven console interface
└── main.py              # Application entry point

tests/
├── unit/
│   ├── test_task.py     # Task model tests
│   └── test_task_manager.py  # Task manager tests
├── integration/
│   ├── test_add_task.py      # Add task flow tests
│   ├── test_view_tasks.py    # View tasks flow tests
│   ├── test_update_task.py   # Update task flow tests
│   ├── test_delete_task.py   # Delete task flow tests
│   └── test_toggle_task.py   # Toggle task flow tests
└── conftest.py          # Test configuration
```

## Testing

To run the tests:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

## Architecture

- **Task Model**: Represents a single todo item with ID, Title, Description, and Completion Status
- **TaskManager Service**: Handles the storage, retrieval, and manipulation of tasks in memory
- **ConsoleInterface**: Manages user interaction through menu or command-driven interface
- **Main**: Application entry point that integrates all components

## Constraints

- Data exists only in memory during the current session (no persistence)
- No external dependencies beyond Python standard library
- Console-based interaction only