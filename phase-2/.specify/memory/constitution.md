<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: All principles and sections from user input
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md - Constitution Check section should align with new principles (✅ reviewed)
  - .specify/templates/spec-template.md - Requirements should align with new constraints (✅ reviewed)
  - .specify/templates/tasks-template.md - Task categorization should reflect new principles (✅ reviewed)
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application (Phase 2 – Hackathon 2) Constitution

## Core Principles

### Security
All user data must be protected via JWT authentication

### Accuracy
API responses must reflect true database state

### Reliability
Endpoints must handle errors gracefully

### Maintainability
Code must follow clean architecture and modular design

### Usability
Frontend must be responsive and intuitive

### Additional Standards
Backend: FastAPI + SQLModel with Neon PostgreSQL, Frontend: Next.js 16+ (App Router), responsive design, Authentication: Better Auth with JWT plugin, API: RESTful endpoints with proper HTTP status codes, Data validation: All inputs validated both client and server-side, Error handling: Consistent error responses and logging, Testing: Minimal functional tests for API endpoints, Security: JWT verification, user isolation, no exposed secrets, Version control: All code in Git repository with clear commit messages

## Constraints

Backend must enforce task ownership per user, JWT tokens expire after 7 days, All frontend API calls must include Authorization header, Database schema must include task and user tables with proper relations, No manual coding: Use Claude Code and Spec-Kit Plus workflow, Multi-user support required, Full CRUD for tasks + toggle completion, Deployment-ready code structure

## Success Criteria

All endpoints return correct data filtered by authenticated user, JWT authentication fully integrated and validated, Frontend consumes secured APIs correctly, Task CRUD operations functional and persistent in database, Responsive UI for desktop and mobile, All planned features implemented via Spec-Kit Plus workflow, Secure handling of secrets and environment variables, No runtime errors during usage by multiple users

## Governance

All implementations must follow the specified technology stack (FastAPI + SQLModel + Neon PostgreSQL for backend, Next.js 16+ for frontend, Better Auth for authentication), JWT authentication must be properly implemented with token verification, Code must be version controlled with clear commit messages, All API endpoints must be tested for proper user isolation

**Version**: 1.0.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14