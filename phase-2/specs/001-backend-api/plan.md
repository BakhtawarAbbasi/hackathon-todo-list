# Implementation Plan: Backend API & Database

**Feature Branch**: `001-backend-api`
**Created**: 2026-02-10
**Status**: Draft
**Input**: User description: "Todo Full-Stack Web App – Spec 1: Backend API & Database

Objective: Transform the console app tasks into a persistent multi-user backend API"

## Technical Context

**Architecture**: FastAPI backend with SQLModel ORM and Neon PostgreSQL database
**Authentication**: JWT integration (handled in Spec 2)
**API Design**: RESTful endpoints with proper HTTP status codes
**Data Model**: Users and Tasks with one-to-many relationship
**Deployment**: Production-ready structure with modular organization

**NEEDS CLARIFICATION**:
- Database connection string format and environment variable naming
- JWT token extraction method (header format, middleware setup)
- Error response format and structure
- Database migration strategy (initial setup vs ongoing)
- Testing framework and coverage requirements

## Constitution Check

**Security**: All user data protected via JWT authentication - ✅
**Accuracy**: API responses reflect true database state - ✅
**Reliability**: Endpoints handle errors gracefully - ✅
**Maintainability**: Clean architecture and modular design - ✅
**Usability**: Backend API should be intuitive for frontend consumption - ✅

**Constitution Compliance**: All core principles are satisfied by the proposed implementation approach.

## Gates

**Technical Feasibility**: ✅ FastAPI + SQLModel + Neon PostgreSQL is a proven stack
**Security Requirements**: ✅ JWT integration and user isolation enforced
**Performance Requirements**: ✅ REST endpoints with proper status codes
**Maintainability**: ✅ Modular structure with clear separation of concerns
**Testing Requirements**: ✅ Functional testing for all endpoints

**All gates passed - implementation is approved**

## Phase 0: Research & Analysis

### Research Tasks

1. **Research FastAPI + SQLModel best practices**
   - Task: "Research FastAPI best practices for production applications"
   - Task: "Research SQLModel ORM patterns and relationship management"
   - Task: "Research Neon PostgreSQL connection and configuration"

2. **Research JWT integration patterns**
   - Task: "Research JWT token extraction and validation in FastAPI"
   - Task: "Research user authentication middleware patterns"

3. **Research testing strategies**
   - Task: "Research FastAPI testing frameworks and patterns"
   - Task: "Research database testing with SQLModel and PostgreSQL"

### Research Findings (to be populated)

**Database Connection**:
- Decision: Use environment variables for database credentials
- Rationale: Security best practices and deployment flexibility
- Format: DATABASE_URL="postgresql://user:password@host:5432/dbname"

**JWT Integration**:
- Decision: FastAPI middleware for token extraction
- Rationale: Centralized authentication handling
- Format: Authorization: Bearer {token}

**Error Response Format**:
- Decision: Consistent JSON error structure
- Rationale: Predictable error handling for frontend
- Structure: {"error": {"code": "string", "message": "string"}}

**Database Migration**:
- Decision: SQLModel's automatic table creation
- Rationale: Simplicity for initial development
- Strategy: Create tables on first run with proper constraints

**Testing Framework**:
- Decision: pytest with FastAPI test client
- Rationale: Industry standard and good integration
- Coverage: All endpoints with success and error scenarios

## Phase 1: Design & Contracts

### Data Model Design

**User Entity**:
- id: UUID (primary key)
- email: String (unique, validated)
- password_hash: String (hashed, never plain text)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-updated)

**Task Entity**:
- id: UUID (primary key)
- title: String (required, max 255 chars)
- description: String (optional, max 1000 chars)
- completed: Boolean (default False)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-updated)
- user_id: UUID (foreign key to User)

**Relationships**:
- User.tasks: One-to-many relationship
- Task.user: Many-to-one relationship

### API Contracts

**Base URL**: `/api/{user_id}`

**GET /api/{user_id}/tasks**
- Purpose: List all tasks for authenticated user
- Response: 200 OK with array of tasks
- Filters: By user_id from JWT

**POST /api/{user_id}/tasks**
- Purpose: Create new task
- Request: {"title": "string", "description": "string"}
- Response: 201 Created with created task
- Validation: Title required, description optional

**GET /api/{user_id}/tasks/{id}**
- Purpose: Get task details by ID
- Response: 200 OK with task details
- Security: Verify task belongs to user

**PUT /api/{user_id}/tasks/{id}**
- Purpose: Update task details
- Request: {"title": "string", "description": "string"}
- Response: 200 OK with updated task
- Validation: Same as POST

**DELETE /api/{user_id}/tasks/{id}**
- Purpose: Delete task
- Response: 204 No Content
- Security: Verify task belongs to user

**PATCH /api/{user_id}/tasks/{id}/complete**
- Purpose: Toggle task completion
- Request: {"completed": true/false}
- Response: 200 OK with updated task

### OpenAPI Schema (to be generated)

```yaml
openapi: 3.0.0
info:
  title: Todo API
  version: 1.0.0
paths:
  /api/{user_id}/tasks:
    get:
      summary: List user tasks
      responses:
        '200':
          description: List of tasks
    post:
      summary: Create task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
      responses:
        '201':
          description: Task created
  # Additional endpoints follow same pattern
```

### Quickstart Guide

**Prerequisites**:
- Python 3.11+
- PostgreSQL database (Neon)
- Environment variables configured

**Setup**:
```bash
# Install dependencies
pip install fastapi uvicorn sqlmodel psycopg2-binary python-dotenv

# Set environment variables
export DATABASE_URL="postgresql://..."
export SECRET_KEY="..."

# Run migrations (automatic)
# Start server
uvicorn main:app --reload
```

**Usage**:
```bash
# Create task
curl -X POST "http://localhost:8000/api/1/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'

# List tasks
curl -X GET "http://localhost:8000/api/1/tasks"
```

## Phase 2: Implementation Tasks

### Task 1: Project Setup (Priority: P1)
- Create project structure: main.py, models/, routes/, db/, tests/
- Initialize FastAPI application
- Install required dependencies
- Setup environment configuration

### Task 2: Database Models (Priority: P1)
- Define User and Task models with SQLModel
- Configure relationships and constraints
- Implement validation rules
- Create database connection module

### Task 3: API Routes Implementation (Priority: P1)
- Implement GET /tasks endpoint
- Implement POST /tasks endpoint
- Implement GET /tasks/{id} endpoint
- Implement PUT /tasks/{id} endpoint
- Implement DELETE /tasks/{id} endpoint
- Implement PATCH /tasks/{id}/complete endpoint

### Task 4: Validation & Error Handling (Priority: P2)
- Implement input validation for all endpoints
- Add proper HTTP status codes
- Create consistent error response format
- Add try-except blocks for database errors

### Task 5: Testing (Priority: P2)
- Write functional tests for all endpoints
- Test success scenarios and error cases
- Verify task ownership and filtering
- Test database persistence

### Task 6: Documentation & Cleanup (Priority: P3)
- Add README.md with API documentation
- Organize code structure
- Add deployment configuration
- Final code review and cleanup

## Dependencies

**Internal Dependencies**:
- Spec 2: JWT authentication integration
- Database credentials from environment

**External Dependencies**:
- FastAPI framework
- SQLModel ORM
- Neon PostgreSQL
- Python 3.11+

## Risks & Mitigations

**Risk**: Database connection failures
- Mitigation: Graceful error handling and retry logic

**Risk**: JWT token extraction issues
- Mitigation: Comprehensive testing and fallback handling

**Risk**: Data consistency problems
- Mitigation: Database constraints and proper transaction handling

**Risk**: Performance bottlenecks
- Mitigation: Proper indexing and query optimization

## Success Metrics

- All endpoints return correct data filtered by authenticated user
- Task CRUD operations functional and persistent in database
- Proper HTTP status codes and error handling
- Clean, maintainable code structure
- All tests pass successfully

## Completion Criteria

- [ ] All 6 API endpoints implemented and tested
- [ ] Database models correctly defined and connected
- [ ] Proper error handling and validation implemented
- [ ] JWT authentication integrated (via Spec 2)
- [ ] Code follows modular structure and clean architecture
- [ ] Documentation complete and deployment-ready
- [ ] All tests pass successfully