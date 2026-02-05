---
id: 1
title: Update project constitution
stage: constitution
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: dell
command: /sp.constitution
labels: [constitution, project-setup]
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

Project: Phase II – Todo Full-Stack Web Application

Objective:
Transform the Phase I in-memory console Todo application into a modern, multi-user,
full-stack web application with persistent storage using Spec-Driven Development.                                                                    Core Principles:
- Spec-driven development is mandatory (Specify → Plan → Tasks → Implement)
- No manual code writing by the developer
- Claude Code is the sole code generator
- Backend and frontend must be independently verifiable
- Security and user isolation are non-negotiable

Key Standards:
- All functionality must originate from written specs
- REST APIs must be stateless and JWT-secured
- Each user can only access their own data
- Frontend and backend must share authentication context via JWT
- Code changes require spec refinement, not direct edits

Technology Constraints:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Spec Tooling: Claude Code + Spec-Kit Plus                                                                                                          Security Rules:
- Every API request must include a valid JWT
- Backend must verify JWT using a shared secret
- Requests without valid authentication must return 401
- Task ownership must be enforced at API and database level
3. Technology Stack (REQUIRED)
Frontend

Framework: Next.js 16+ (App Router - REQUIRED)
Language: TypeScript
Styling: Tailwind CSS (core utility classes only)
Authentication: Better Auth with JWT tokens

Backend

Framework: Python FastAPI
ORM: SQLModel
Database: Neon Serverless PostgreSQL
API Style: RESTful JSON endpoints

Development Tools

Spec Management: Spec-Kit Plus
AI Coding: Claude Code
Package Manager: UV (Python)

4. Security Requirements

Authentication: Every API endpoint requires valid JWT token
Authorization: User isolation - users only see their own tasks
Token Management: Shared secret (BETTER_AUTH_SECRET) between frontend/backend
Error Handling: Return 401 Unauthorized for invalid/missing tokens
User Filtering: All queries filtered by authenticated user ID

5. Data Persistence Standards

Database: Neon Serverless PostgreSQL (REQUIRED)
ORM: SQLModel for all database operations
Migrations: Track all schema changes
Connection: Use DATABASE_URL environment variable
User Isolation: All tasks assoc
Repository Constraints:
- Monorepo structure
- Separate frontend and backend folders
- Specs must be versioned and traceable
- CLAUDE.md files guide Claude Code behavior

Success Criteria:
- All 5 basic Todo features work end-to-end
- Persistent storage confirmed via database
- Authentication fully enforced
- Spec-driven workflow is clearly demonstrable

## Response snapshot

Updated the project constitution at `.specify/memory/constitution.md` with the following:
- Created new version 1.0.0 constitution for Todo Full-Stack Web Application
- Defined 5 core principles: Spec-Driven Development, Technology Stack Compliance, Security-First Architecture, Data Persistence Standards, Authentication Context Sharing
- Added detailed Technology Stack section with frontend, backend, and development tools
- Established Security Requirements with authentication and authorization rules
- Defined Data Persistence Standards for Neon PostgreSQL and SQLModel
- Set Repository Constraints for project structure and development workflow
- Governance section establishes constitution as supreme authority

## Outcome

- ✅ Impact: Created comprehensive constitution governing the entire Todo Full-Stack Web Application project
- 🧪 Tests: None required for constitution update
- 📁 Files: Updated `.specify/memory/constitution.md` with new project constitution
- 🔄 Next prompts: Ready to begin spec-driven development workflow
- 🧠 Reflection: Constitution provides clear governance framework for spec-driven development with security-first approach

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Not applicable