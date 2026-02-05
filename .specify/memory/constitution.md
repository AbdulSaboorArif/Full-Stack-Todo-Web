<!-- Sync Impact Report: Version change: 1.0.0 → 1.1.0 Modified principles: None Added sections: None Removed sections: None Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md Follow-up TODOs: None -->
# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (MANDATORY)

All functionality must originate from written specifications. No manual code writing by the developer. Claude Code is  
the sole code generator. Backend and frontend must be independently verifiable. Security and user isolation are  
non-negotiable.

### II. Technology Stack Compliance (REQUIRED)

**Frontend:**  
- Next.js 16+ (App Router - REQUIRED)  
- TypeScript  
- Tailwind CSS (core utility classes only)  
- Better Auth with JWT tokens  

**Backend:**  
- Python FastAPI  
- SQLModel  
- Neon Serverless PostgreSQL  
- RESTful JSON endpoints  

**Spec Management & Tooling:**  
- Spec-Kit Plus  
- AI Coding: Claude Code  
- Package Manager: UV (Python)

### III. Security-First Architecture (NON-NEGOTIABLE)

Every API request must include a valid JWT token. Backend must verify JWT using a shared secret. Requests without valid  
authentication must return **401 Unauthorized**. Task ownership must be enforced at API and database level.  
User isolation is mandatory — users may only access their own tasks.

### IV. Data Persistence Standards (REQUIRED)

- **Database:** Neon Serverless PostgreSQL (REQUIRED)  
- **ORM:** SQLModel for all database operations  
- **Migrations:** All schema changes must be tracked  
- **Connection:** Use `DATABASE_URL` environment variable  
- **User Isolation:** All tasks associated with authenticated user ID

### V. Authentication Context Sharing (MANDATORY)

- User registration and authentication required  
- Multi-user todo management  
- Frontend and backend must share authentication context via JWT  
- Frontend → API call includes JWT in `Authorization: Bearer <token>`  
- Backend → Extracts token, verifies signature, identifies user

## Technology Stack

### Frontend Layer
- Framework: Next.js 16+ (App Router - REQUIRED)
- Language: TypeScript
- Styling: Tailwind CSS (core utility classes only)
- Authentication: Better Auth with JWT tokens

### Backend Layer
- Framework: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- API Style: RESTful JSON endpoints

### Development Tools
- Spec Management: Spec-Kit Plus
- AI Coding: Claude Code
- Package Manager: UV (Python)

## Security Requirements

### Authentication Rules
- Every API endpoint requires a valid JWT token
- Backend must verify JWT using shared secret (`BETTER_AUTH_SECRET`)
- Requests without valid authentication must return **401 Unauthorized**
- Task ownership must be enforced at API and database level

### Authorization Rules
- User isolation — users only see their own tasks
- All queries filtered by authenticated user ID
- Backend decodes token to obtain user ID, email, etc.
- User filtering enforced across all database queries

## Data Persistence Standards

### Database Configuration
- Database: Neon Serverless PostgreSQL (REQUIRED)
- ORM: SQLModel
- Migrations: Required for all schema changes
- Connection: `DATABASE_URL` environment variable

### User Data Isolation
- All tasks linked to authenticated user ID
- Enforcement at both API and database layers
- Persistent storage via Neon database

## Repository Constraints

### Project Structure
- Monorepo structure
- Separate frontend and backend directories
- Versioned and traceable specifications
- `CLAUDE.md` files guide Claude Code behavior

### Development Workflow
- Spec-driven development is mandatory: **Specify → Plan → Tasks → Implement**
- No direct code edits without spec updates
- REST APIs must be stateless and JWT-secured

## Governance

This constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan.  
All pull requests and reviews must verify compliance. Complexity must be justified.

**Version:** 1.1.0  
**Ratified:** 2026-02-03  
**Last Amended:** 2026-02-03
