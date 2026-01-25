# Data Model: Phase I Console Todo App

## Task Entity

**Definition**: Represents a single todo item with ID, Title, Description, and Completion Status

**Attributes**:
- `id`: Integer - Unique identifier for the task (automatically assigned)
- `title`: String - Title/description of the task (required, non-empty)
- `description`: String - Detailed description of the task (optional)
- `completed`: Boolean - Completion status of the task (default: False/incomplete)

**Validation Rules**:
- ID must be unique within the session
- Title must be provided and non-empty
- ID must be positive integer
- Completed status must be boolean value

**State Transitions**:
- `incomplete` (False) → `complete` (True) via toggle operation
- `complete` (True) → `incomplete` (False) via toggle operation

## Task Collection

**Definition**: In-memory storage for tasks during the session

**Operations**:
- Add new task to collection
- Retrieve all tasks
- Retrieve specific task by ID
- Update task by ID
- Delete task by ID
- Toggle completion status by ID

**Constraints**:
- All data exists only in memory during current session
- No persistence between application runs
- Tasks are scoped to current session only

## Session State

**Definition**: Container for the current application state

**Components**:
- Collection of tasks (list/dictionary)
- Next available ID counter
- Application state (running/stopped)

**Lifecycle**:
- Initialized when application starts
- Maintained during user interaction
- Destroyed when application exits