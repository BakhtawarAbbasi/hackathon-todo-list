---
id: 2
title: Create Specification
stage: spec
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: console-todo-app
branch: 001-console-todo-app
user: user
command: /sp.specify
labels: [specification, todo-app, console-app]
links:
  spec: specs/001-console-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-console-todo-app/spec.md
 - specs/001-console-todo-app/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
Phase I — In-Memory Python Console Todo App

Objective:
Define all requirements for a Python console-based, in-memory Todo app using Spec-Driven Development with Claude Code.
Target Users:
- Hackathon evaluators
- Developers running the console app
Mandatory Features:
1. Add Task: ID, Title, Description, Completion status (default: incomplete)
2. View Task List: Show ID, Title, Description, Status
3. Update Task: Edit Title & Description by ID
4. Delete Task: Remove task by ID
5. Toggle Complete/Incomplete by ID

Interaction & UX:
- Menu or command-driven console
- Clear prompts & messages
- Graceful handling of invalid input

Technical Constraints:
- Python 3.13+, UV environment
- In-memory only (no DB/files)
- Modular clean code: Task model, Manager, CLI
Error Handling:
- Invalid IDs, empty lists, duplicate operations, empty inputs

Deliverables:
- /src folder with code
- Specs history folder
- README.md & CLAUDE.md

Out of Scope:
- Databases, web/mobile UI, AI chatbot, cloud deployment

Success Criteria:
- All 5 features work
- Runs without crashes
- Matches spec exactly
```

## Response snapshot

Created comprehensive specification for the Phase I In-Memory Python Console Todo App. The spec includes all 5 mandatory features (Add, View, Update, Delete, Toggle tasks) with detailed user scenarios, functional requirements, key entities, and success criteria. The specification follows the template structure and is ready for the planning phase.

## Outcome

- ✅ Impact: Complete specification created for console todo app
- 🧪 Tests: none
- 📁 Files: specs/001-console-todo-app/spec.md, specs/001-console-todo-app/checklists/requirements.md
- 🔁 Next prompts: Proceed to planning phase with /sp.plan
- 🧠 Reflection: Specification covers all mandatory features with clear acceptance scenarios

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning implementation