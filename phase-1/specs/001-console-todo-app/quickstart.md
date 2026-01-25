# Quickstart Guide: Console Todo App

## Prerequisites

- Python 3.13+ installed
- UV package manager installed (optional, for virtual environment management)

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd hackathon-todo-list
   ```

2. Create virtual environment (recommended):
   ```bash
   uv venv  # if using UV
   # OR
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   venv\Scripts\activate  # Windows
   ```

3. Navigate to project directory:
   ```bash
   cd hackathon-todo-list
   ```

## Running the Application

1. Execute the main application:
   ```bash
   python src/main.py
   ```

2. The console application will start and present a menu with options to:
   - Add a new task
   - View all tasks
   - Update an existing task
   - Delete a task
   - Toggle task completion status
   - Exit the application

## Basic Usage

1. **Adding a Task**: Select option 1, enter title and description when prompted
2. **Viewing Tasks**: Select option 2 to see all tasks with their status
3. **Updating a Task**: Select option 3, provide task ID and new details
4. **Deleting a Task**: Select option 4, provide the task ID
5. **Toggling Completion**: Select option 5, provide task ID to toggle status
6. **Exiting**: Select option 6 or use Ctrl+C to quit

## Example Session

```
Welcome to the Todo App!
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit
Choose an option: 1
Enter task title: Buy groceries
Enter task description: Milk, bread, eggs
Task added successfully with ID: 1

Choose an option: 2
Tasks:
ID: 1 | Title: Buy groceries | Description: Milk, bread, eggs | Status: Incomplete
```

## Testing

Run the test suite to verify functionality:

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```