---
# Research: Todo Full-Stack Web Application

**Branch**: `1-todo-full-stack` | **Date**: 2026-02-03 | **Spec**: `specs/1-todo-full-stack/spec.md`
**Input**: Feature specification from `/specs/1-todo-full-stack/spec.md`

## Technical Context Resolution

### Language/Version
- **Resolution**: Python 3.11+ (FastAPI backend), TypeScript 5.0+ (Next.js frontend)
- **Rationale**: FastAPI requires Python 3.7+, Next.js requires Node.js 18+. Python 3.11+ provides performance improvements and latest features.

### Primary Dependencies
- **Resolution**: FastAPI, SQLModel, Better Auth, Next.js 16+, Tailwind CSS
- **Rationale**: Constitution mandates FastAPI, SQLModel, Better Auth for backend; Next.js 16+ with App Router and Tailwind CSS for frontend.

### Storage
- **Resolution**: Neon Serverless PostgreSQL
- **Rationale**: Constitution mandates Neon Serverless PostgreSQL as the database solution.

### Testing
- **Resolution**: pytest (backend), Jest/React Testing Library (frontend)
- **Rationale**: pytest is standard for Python/FastAPI, Jest/React Testing Library for Next.js frontend testing.

### Target Platform
- **Resolution**: Web application (multi-platform browser support)
- **Rationale**: The specification clearly states "web-based frontend" and "web interface for all task operations".

### Project Type
- **Resolution**: Web application (frontend + backend)
- **Rationale**: The architecture consists of separate frontend and backend services.

### Performance Goals
- **Resolution**: <2 seconds API response time, support 10+ concurrent users
- **Rationale**: Specification states "API response time is under 2 seconds for all endpoints under normal load" and "supports multiple concurrent users without performance degradation".

### Constraints
- **Resolution**: <2 seconds p95 latency, secure JWT authentication, user isolation
- **Rationale**: Performance constraint from spec, security constraints from constitution (JWT authentication, user isolation).

### Scale/Scope
- **Resolution**: Multi-user todo application with individual task management
- **Rationale**: Specification describes "multi-user Todo web application" with "personal task lists" and "individual task management".

## Research Findings

### Better Auth Integration
- **Decision**: Use Better Auth with JWT plugin
- **Rationale**: Constitution mandates Better Auth with JWT tokens. Better Auth provides comprehensive authentication including signup, signin, session management, and JWT token issuance.
- **Alternatives considered**: Custom JWT implementation, Auth0, NextAuth.js
- **Why chosen**: Better Auth is specifically mentioned in constitution and provides the required JWT functionality with minimal configuration.

### Next.js 16+ App Router
- **Decision**: Use Next.js 16+ with App Router
- **Rationale**: Constitution mandates Next.js 16+ with App Router for the frontend.
- **Alternatives considered**: Pages router, Remix, SvelteKit
- **Why chosen**: Next.js 16+ with App Router is explicitly required by the constitution and provides modern React patterns.

### SQLModel for Database Operations
- **Decision**: Use SQLModel for all database operations
- **Rationale**: Constitution mandates SQLModel as the ORM.
- **Alternatives considered**: SQLAlchemy, Tortoise ORM, Pydantic models with raw SQL
- **Why chosen**: SQLModel is specifically required by the constitution and provides seamless integration with FastAPI and Pydantic models.

### JWT Token Sharing
- **Decision**: Shared JWT secret between frontend and backend
- **Rationale**: Constitution mandates JWT-based authentication with shared secret.
- **Implementation**: Use BETTER_AUTH_SECRET environment variable consistently across both services.
- **Security**: Tokens must be stored securely in browser (HTTP-only cookies or secure storage).

### User Isolation Implementation
- **Decision**: Enforce user isolation at API and database level
- **Rationale**: Constitution mandates user isolation - users only see their own tasks.
- **Implementation**: Filter all queries by authenticated user ID, validate user_id in request path matches token payload.

## Dependencies and Integration Points

### Frontend Dependencies
- next: ^16.0.0
- react: ^18.0.0
- @better-auth/nextjs: ^1.0.0
- @better-auth/jwt: ^1.0.0
- tailwindcss: ^3.0.0
- @types/node: ^18.0.0
- @types/react: ^18.0.0

### Backend Dependencies
- fastapi: ^0.104.0
- sqlmodel: ^0.1.0
- better-auth: ^1.0.0
- python-multipart: ^0.0.6
- uvicorn: ^0.24.0
- python-jose: ^3.3.0
- python-dotenv: ^1.0.0

### Development Dependencies
- pytest: ^7.0.0
- pytest-asyncio: ^0.21.0
- httpx: ^0.25.0
- @testing-library/react: ^14.0.0
- jest: ^29.0.0

## Integration Requirements

### Frontend→Backend Communication
- All API calls must include Authorization: Bearer {token} header
- Base URL configuration for API endpoints
- Error handling for authentication failures (401)
- Automatic token refresh if needed

### Backend→Database Communication
- Connection string from DATABASE_URL environment variable
- SQLModel session management per request
- User isolation enforced in all queries
- Proper error handling and logging

### Authentication Flow
- Frontend: Better Auth handles signup/signin and JWT issuance
- Frontend: Store token securely and attach to API calls
- Backend: Verify JWT signature using shared secret
- Backend: Extract user ID from token payload
- Backend: Validate user_id in request path matches token payload

## Risks and Mitigations

### Security Risks
- **Risk**: JWT token theft or misuse
- **Mitigation**: Use secure storage, HTTPS only, short token expiration, proper CORS configuration

### Performance Risks
- **Risk**: Database query performance with many users/tasks
- **Mitigation**: Proper indexing, connection pooling, query optimization

### Integration Risks
- **Risk**: Frontend-backend authentication mismatch
- **Mitigation**: Shared secret configuration, thorough testing of authentication flow

---

*Research complete. All technical context clarifications resolved.*