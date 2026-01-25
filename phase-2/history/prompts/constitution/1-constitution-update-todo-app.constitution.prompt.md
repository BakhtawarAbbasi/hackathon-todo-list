---
id: 1
title: constitution-update-todo-app
stage: constitution
date: 2026-01-14
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 001-console-todo-app
user: user
command: /sp.constitution
labels: [constitution, todo-app, hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
/sp.constitution

Project: Todo Full-Stack Web Application (Phase 2 – Hackathon 2)

Core principles:
- Security: All user data must be protected via JWT authentication
- Accuracy: API responses must reflect true database state
- Reliability: Endpoints must handle errors gracefully
- Maintainability: Code must follow clean architecture and modular design
- Usability: Frontend must be responsive and intuitive

Key standards:
- Backend: FastAPI + SQLModel with Neon PostgreSQL
- Frontend: Next.js 16+ (App Router), responsive design
- Authentication: Better Auth with JWT plugin
- API: RESTful endpoints with proper HTTP status codes
- Data validation: All inputs validated both client and server-side
- Error handling: Consistent error responses and logging
- Testing: Minimal functional tests for API endpoints
- Security: JWT verification, user isolation, no exposed secrets
- Version control: All code in Git repository with clear commit messages

Constraints:
- Backend must enforce task ownership per user
- JWT tokens expire after 7 days
- All frontend API calls must include Authorization header
- Database schema must include task and user tables with proper relations
- No manual coding: Use Claude Code and Spec-Kit Plus workflow
- Multi-user support required
- Full CRUD for tasks + toggle completion
- Deployment-ready code structure

Success criteria:
- All endpoints return correct data filtered by authenticated user
- JWT authentication fully integrated and validated
- Frontend consumes secured APIs correctly
- Task CRUD operations functional and persistent in database
- Responsive UI for desktop and mobile
- All planned features implemented via Spec-Kit Plus workflow
- Secure handling of secrets and environment variables
- No runtime errors during usage by multiple users
```

## Response snapshot

Updated the project constitution with all specified principles, standards, constraints, and success criteria for the Todo Full-Stack Web Application project. Created a comprehensive constitution document with 5 core principles plus additional standards, constraints and success criteria sections as specified.

## Outcome

- ✅ Impact: Updated constitution file with all required principles and guidelines
- 🧪 Tests: No tests required for this documentation update
- 📁 Files: .specify/memory/constitution.md updated with complete constitution
- 🔁 Next prompts: Ready to proceed with spec, plan and tasks creation
- 🧠 Reflection: Successfully created comprehensive constitution from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution