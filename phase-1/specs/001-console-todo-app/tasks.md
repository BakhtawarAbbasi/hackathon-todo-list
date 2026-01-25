---
description: "Task list for Phase I Console Todo App implementation"
---

# Tasks: Console Todo App

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as specified in the feature requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 [P] Create src/ directory structure (models/, services/, cli/)
- [X] T003 [P] Create tests/ directory structure (unit/, integration/)
- [X] T004 Initialize Python project with basic configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Task model in src/models/task.py
- [X] T006 Create TaskManager service in src/services/task_manager.py
- [X] T007 Create base console interface in src/cli/console_interface.py
- [X] T008 Create main application entry point in src/main.py
- [X] T009 Create base test configuration in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with title, description, and default incomplete status

**Independent Test**: Can be fully tested by launching the application, selecting the add task option, providing a title and description, and verifying that the task appears in the list with a unique ID and default incomplete status.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [X] T011 [P] [US1] Unit test for add_task functionality in tests/unit/test_task_manager.py
- [X] T012 [P] [US1] Integration test for add task flow in tests/integration/test_add_task.py

### Implementation for User Story 1

- [X] T013 [P] [US1] Implement Task model with ID, title, description, and completion status in src/models/task.py
- [X] T014 [US1] Implement add_task method in TaskManager service in src/services/task_manager.py
- [X] T015 [US1] Implement add_task_prompt in ConsoleInterface in src/cli/console_interface.py
- [X] T016 [US1] Add error handling for empty title/description in src/services/task_manager.py
- [X] T017 [US1] Add unique ID assignment logic in src/services/task_manager.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Allow users to see all their current tasks with ID, title, description, and status

**Independent Test**: Can be fully tested by adding at least one task and then viewing the task list to verify all tasks are displayed with correct information.

### Tests for User Story 2 ⚠️

- [X] T018 [P] [US2] Unit test for get_all_tasks in tests/unit/test_task_manager.py
- [X] T019 [P] [US2] Integration test for view tasks flow in tests/integration/test_view_tasks.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Implement get_all_tasks method in TaskManager service in src/services/task_manager.py
- [X] T021 [US2] Implement get_task method in TaskManager service in src/services/task_manager.py
- [X] T022 [US2] Implement view_tasks_prompt in ConsoleInterface in src/cli/console_interface.py
- [X] T023 [US2] Implement formatted display of tasks in src/cli/console_interface.py
- [X] T024 [US2] Handle empty task list case in src/cli/console_interface.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Allow users to modify an existing task's title and description by providing the task ID

**Independent Test**: Can be fully tested by adding a task, updating its title and description, and verifying the changes are reflected when viewing the task list.

### Tests for User Story 3 ⚠️

- [X] T025 [P] [US3] Unit test for update_task in tests/unit/test_task_manager.py
- [X] T026 [P] [US3] Integration test for update task flow in tests/integration/test_update_task.py

### Implementation for User Story 3

- [X] T027 [P] [US3] Implement update_task method in TaskManager service in src/services/task_manager.py
- [X] T028 [US3] Implement update_task_prompt in ConsoleInterface in src/cli/console_interface.py
- [X] T029 [US3] Add validation for task existence in src/services/task_manager.py
- [X] T030 [US3] Add error handling for invalid task ID in src/cli/console_interface.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: Allow users to remove a task from the system by providing the task ID

**Independent Test**: Can be fully tested by adding a task, deleting it, and verifying it no longer appears in the task list.

### Tests for User Story 4 ⚠️

- [X] T031 [P] [US4] Unit test for delete_task in tests/unit/test_task_manager.py
- [X] T032 [P] [US4] Integration test for delete task flow in tests/integration/test_delete_task.py

### Implementation for User Story 4

- [X] T033 [P] [US4] Implement delete_task method in TaskManager service in src/services/task_manager.py
- [X] T034 [US4] Implement delete_task_prompt in ConsoleInterface in src/cli/console_interface.py
- [X] T035 [US4] Add confirmation prompt for deletion in src/cli/console_interface.py
- [X] T036 [US4] Add error handling for invalid task ID in src/cli/console_interface.py

**Checkpoint**: All user stories should work together

---

## Phase 7: User Story 5 - Toggle Task Completion Status (Priority: P2)

**Goal**: Allow users to mark a task as complete or incomplete by providing the task ID

**Independent Test**: Can be fully tested by adding a task, toggling its status, and verifying the status change when viewing the task list.

### Tests for User Story 5 ⚠️

- [X] T037 [P] [US5] Unit test for toggle_task_status in tests/unit/test_task_manager.py
- [X] T038 [P] [US5] Integration test for toggle task flow in tests/integration/test_toggle_task.py

### Implementation for User Story 5

- [X] T039 [P] [US5] Implement toggle_task_status method in TaskManager service in src/services/task_manager.py
- [X] T040 [US5] Implement toggle_task_prompt in ConsoleInterface in src/cli/console_interface.py
- [X] T041 [US5] Add error handling for invalid task ID in src/cli/console_interface.py
- [X] T042 [US5] Update task display to show completion status in src/cli/console_interface.py

**Checkpoint**: All core functionality should now be implemented

---

## Phase 8: Main Application & Menu Integration

**Goal**: Integrate all user stories into a cohesive menu-driven console application

- [X] T043 Create main menu display in src/main.py
- [X] T044 Integrate all user story functions into main menu loop in src/main.py
- [X] T045 Implement menu navigation and input handling in src/main.py
- [X] T046 Add graceful exit functionality in src/main.py

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T047 [P] Add comprehensive error handling throughout application
- [X] T048 [P] Add input validation for all user inputs
- [X] T049 [P] Improve user experience with better prompts and messages
- [X] T050 [P] Add README.md with setup and usage instructions
- [X] T051 [P] Add CLAUDE.md with project information
- [X] T052 [P] Add additional unit tests in tests/unit/
- [X] T053 Run quickstart.md validation
- [X] T054 [P] Add documentation in src/ docstrings

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Menu Integration (Phase 8)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Task model in tests/unit/test_task.py"
Task: "Unit test for add_task functionality in tests/unit/test_task_manager.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with ID, title, description, and completion status in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence