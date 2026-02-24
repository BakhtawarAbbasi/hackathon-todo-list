# Todo Backend API

A FastAPI-based backend service for managing user tasks with Neon PostgreSQL database.

## Overview

This backend API provides a RESTful interface for managing user tasks. It includes all basic CRUD operations with proper user isolation, ensuring that users can only access their own tasks.

## Features

- **RESTful API**: Clean, predictable endpoints for all operations
- **User Isolation**: Tasks are isolated by user ID to ensure privacy
- **Soft Deletion**: Tasks are soft-deleted to preserve data integrity
- **Pagination & Sorting**: Built-in support for paginating and sorting task lists
- **Error Handling**: Consistent error response format
- **Input Validation**: Comprehensive input validation using Pydantic

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Validation**: Pydantic
- **Testing**: pytest

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

## Configuration

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/todo_db"

# Application Configuration
SECRET_KEY="your-secret-key-here"
PORT=8000

# Environment
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
```

## API Endpoints

### Authentication

> Note: Authentication is handled separately using Better Auth (JWT tokens). All endpoints expect a valid JWT token in the Authorization header.

### Base URL
```
/api/{user_id}/
```

### Tasks Endpoints

#### List User Tasks
```
GET /api/{user_id}/tasks/
```

**Parameters:**
- `skip` (optional): Number of tasks to skip (for pagination)
- `limit` (optional): Maximum number of tasks to return (default: 100)
- `sort_by` (optional): Field to sort by (created_at, updated_at, title; default: created_at)
- `order` (optional): Sort order (asc, desc; default: desc)

**Response:** Array of Task objects

#### Create New Task
```
POST /api/{user_id}/tasks/
```

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Task description (optional)"
}
```

**Response:** Created Task object

#### Get Specific Task
> Note: Currently not implemented as a separate endpoint since we only have list functionality

#### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
```

**Request Body:**
```json
{
  "title": "Updated title (optional)",
  "description": "Updated description (optional)",
  "completed": true (optional)
}
```

**Response:** Updated Task object

#### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{task_id}/complete
```

**Response:** Updated Task object with toggled completion status

#### Delete Task
```
DELETE /api/{user_id}/tasks/{task_id}
```

**Response:** 204 No Content on success

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "todo-backend",
  "version": "1.0.0"
}
```

## Running the Application

### Development
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_module.py
```

## Environment Variables

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT signing (if implemented)
- `PORT`: Port to run the application on
- `ENVIRONMENT`: Environment mode (development, production)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Database Schema

### Users Table
- `id`: UUID (Primary Key)
- `email`: String (Unique, Not Null)
- `password_hash`: String (Not Null)
- `created_at`: DateTime (Not Null)
- `updated_at`: DateTime (Not Null)

### Tasks Table
- `id`: UUID (Primary Key)
- `title`: String (Not Null, Max Length: 255)
- `description`: String (Optional, Max Length: 1000)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Not Null)
- `updated_at`: DateTime (Not Null)
- `is_deleted`: Boolean (Default: False)
- `deleted_at`: DateTime (Optional)
- `user_id`: UUID (Foreign Key to Users, Not Null)

## Error Handling

The API returns consistent error responses in the following format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": []
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR`: 422 - Request validation failed
- `RESOURCE_NOT_FOUND`: 404 - Resource doesn't exist
- `UNAUTHORIZED_ACCESS`: 403 - Access denied
- `DATABASE_ERROR`: 500 - Database operation failed
- `INTERNAL_ERROR`: 500 - Unexpected server error

## Security

- User data is isolated by user ID
- Input validation prevents injection attacks
- Soft deletion preserves data integrity
- Consistent error handling prevents information leakage

## Deployment

This application can be deployed to any platform that supports Python applications (Heroku, AWS, Google Cloud, etc.).

### Docker Support
A Dockerfile is included for containerized deployments.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License