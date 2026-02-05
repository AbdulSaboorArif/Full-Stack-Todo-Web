# Skill: FastAPI Backend Skill – REST APIs, Validation, Auth Integration, DB Interaction

## Purpose

This skill defines how the backend of the **Hackathon II – Evolution of Todo** project must be implemented using **FastAPI + SQLModel + Neon PostgreSQL**, under a fully **spec-driven development** process (Spec-Kit Plus + Claude Code, no manual coding).  

Any agent using this skill is responsible for turning the specs in `/specs/**` into a clean, secure, and well-structured FastAPI backend that exposes the Todo REST API, validates all inputs/outputs, integrates JWT auth from Better Auth, and interacts with Neon via SQLModel. [file:55][web:52]

---

## Alignment with Hackathon Requirements

This skill **must** satisfy the following official constraints:

- Follow the **Agentic Dev Stack** loop:  
  `Specify → Plan → Tasks → Implement` (no direct “vibe coding”). [file:55]
- Implement at least the **Basic Level features** in Phase II as REST APIs:  
  Add, Delete, Update, View, Mark Complete. [file:55]
- Use the mandated stack for Phase II:  
  - Backend: **Python FastAPI**  
  - ORM: **SQLModel**  
  - Database: **Neon Serverless PostgreSQL**  
  - Auth: **Better Auth with JWT**  
  - Specs: **Spec‑Kit Plus**, specs in `/specs/**`. [file:55]
- Respect the **monorepo structure** and backend conventions defined in:  
  - `/.spec-kit/config.yaml`  
  - `/CLAUDE.md`  
  - `/backend/CLAUDE.md`  
  - `/specs/api/rest-endpoints.md`  
  - `/specs/database/schema.md`  
  - `/specs/features/task-crud.md`  
  - `/specs/features/authentication.md`. [file:55]

This skill does **not** design schema (Database Skill) or auth flows (Auth Skill) but must consume both correctly.

---

## Responsibilities of FastAPI Backend Skill

### 1. Implement REST API Endpoints (Phase II baseline)

Implement all Todo REST endpoints as described in the specs, using FastAPI routers under the `/api/` prefix. [file:55][web:52]

**User-scoped endpoints (Phase II spec):**

- `GET  /api/{user_id}/tasks` – List all tasks for the authenticated user.  
- `POST /api/{user_id}/tasks` – Create a new task.  
- `GET  /api/{user_id}/tasks/{id}` – Get task details.  
- `PUT  /api/{user_id}/tasks/{id}` – Update a task.  
- `DELETE /api/{user_id}/tasks/{id}` – Delete a task.  
- `PATCH /api/{user_id}/tasks/{id}/complete` – Toggle completion. [file:55]

**API implementation rules:**

- All routes live in `backend/app/routes/` (e.g. `tasks.py`) and are included from `backend/app/main.py`. [file:55]
- All endpoints are **authenticated**: they must reject requests without a valid JWT (`401`) or with mismatched `user_id` (`403`). [file:55]
- All endpoints must return **JSON**, using FastAPI’s automatic serialization.

### 2. Request Validation

Use Pydantic/SQLModel models to enforce strong validation on all incoming data. [web:39][web:50]

**Bodies:**

- Define request models in `backend/app/schemas.py`, e.g.:
  - `TaskCreate` – required `title` (1–200 chars), optional `description` (≤1000 chars). [file:55]
  - `TaskUpdate` – updateable fields such as `title`, `description`, `completed`.
- Enforce constraints from `specs/features/task-crud.md` and `specs/api/rest-endpoints.md`. [file:55]

**Params:**

- Path parameters:
  - `user_id` – string user identifier (matching Better Auth `users.id`). [file:55]
  - `id` – integer task ID.
- Query parameters (per spec when using `/api/tasks` or phase-II `/api/{user_id}/tasks`):
  - `status`: `"all" | "pending | "completed"`.  
  - `sort`: `"created" | "title" | "due_date"` (when due date exists). [file:55][web:39]

Use FastAPI validation so invalid values produce a `422 Unprocessable Entity` with structured errors.

### 3. Response Models and Output Validation

Define explicit response models and use them as `response_model=...` on all endpoints. [web:48]

- `TaskRead` – representation of a task returned to clients:
  - `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`, and any future fields like `due_date`. [file:55]
- For list endpoints, return `List[TaskRead]` or a typed wrapper.

Rules:

- Only expose safe fields; never return internal secrets or raw tokens.
- Keep response structure consistent across endpoints and specs.
- Use proper status codes:
  - `200` for successful reads/updates.
  - `201` for creates.
  - `204` for deletions with no body.
  - `404` when resource not found.
  - `401`/`403` for auth issues.
  - `422` for validation failures. [web:48]

### 4. Auth Integration (JWT from Better Auth)

Integrate JWTs issued by Better Auth on the frontend, without re‑implementing login/sign‑up logic. [file:55][web:51]

**Token expectations (from Auth Skill + spec):**

- JWT includes at least `user_id`, `email`, and `exp` (expiry). [file:55]
- Signed with a shared secret `BETTER_AUTH_SECRET` configured in environment variables for both frontend and backend. [file:55]

**Backend behavior:**

- Implement a reusable dependency, e.g. `get_current_user`, in `backend/app/dependencies.py` or `auth.py`:
  - Read `Authorization: Bearer <token>` header.
  - Verify signature using `BETTER_AUTH_SECRET`.
  - Check expiry; raise `HTTPException(status_code=401)` on failure.
  - Parse claims into a strongly-typed `CurrentUser` model (id + email, at minimum).
- In each route:
  - Depend on `current_user = Depends(get_current_user)`.
  - Compare `current_user.id` with the `user_id` path parameter:
    - If mismatch, raise `403 Forbidden`. [file:55]
  - Use `current_user.id` in database queries to ensure isolation: **never query tasks for a different user**.

### 5. Database Interaction with SQLModel (using Neon)

Use SQLModel and the DB engine from the **Database Agent** to persist and query data in Neon Postgres. [file:55][web:52]

**Setup:**

- `backend/app/db.py`:
  - Create an SQLModel engine using `DATABASE_URL` (Neon connection string from env). [file:55]
  - Provide `get_session()` dependency that yields a session and ensures proper commit/rollback and close.
- `backend/app/models.py`:
  - Use SQLModel models that match `/specs/database/schema.md`, especially the `tasks` table:
    - `id` (PK, integer), `user_id` (FK string → users.id), `title`, `description`, `completed`, `created_at`, `updated_at`. [file:55]

**CRUD operations:**

- All routes inject a session: `session: Session = Depends(get_session)`.
- Queries must **always** filter by `user_id` from JWT, so users cannot access each other’s tasks. [file:55]
- Implement:
  - `list` – filter, search, and sort tasks by status and sort fields, leveraging indexes (`tasks.user_id`, `tasks.completed`). [file:55][web:52]
  - `create` – insert a new `Task` linked to `current_user.id`.
  - `detail` – fetch one task by `id` and `user_id`.
  - `update` – update fields if the task belongs to the user, otherwise 404.
  - `delete` – delete only if the task belongs to the user.
  - `complete toggle` – flip the `completed` flag and update `updated_at`.

Return `404` if a task with the given `id` does not exist for that `user_id`.

### 6. Error Handling and Robustness

- Use `HTTPException` for API-level errors:
  - `404` when task not found for the given user.
  - `400` for invalid state transitions or unsupported parameters.
  - `401` for missing/invalid/expired tokens.
  - `403` when user tries to access another user’s tasks. [web:48]
- Catch database errors where necessary and:
  - Log detailed errors on the server side.
  - Return generic, safe error messages to the client (no connection strings, stack traces, or SQL text).

---

## Code Organization Rules

This skill enforces a standard backend layout (as referenced in `/backend/CLAUDE.md`). [file:55][web:37]

Minimum layout:

- `backend/app/main.py` – FastAPI application creation, router inclusion, middleware (CORS etc.).
- `backend/app/db.py` – DB engine and session dependency for Neon.
- `backend/app/models.py` – SQLModel DB models (sync with `/specs/database/schema.md`).
- `backend/app/schemas.py` – request/response models.
- `backend/app/auth.py` &/or `backend/app/dependencies.py` – JWT verification + current user dependency.
- `backend/app/routes/tasks.py` – all task REST APIs.
- `backend/tests/` – basic tests (optional but encouraged, especially in later phases).

No route handler may:

- Hard-code `DATABASE_URL` (must come from env).
- Perform raw JWT parsing without using the shared auth helper.
- Perform raw SQL that diverges from the schema spec unless explicitly required.

---

## Interaction with Other Skills / Agents

This skill sits inside the **FastAPI Backend Agent** and cooperates with other skills:

- **Auth Skill:**  
  - Source of JWT generation rules and token claims.  
  - Backend must trust and validate tokens according to this spec; must not re‑implement signup/signin. [file:55]
- **Database Skill:**  
  - Source of the canonical schema and DB migration strategy.  
  - Backend must not change table shapes directly; it only uses the SQLModel models that conform to `schema.md`. [file:55]
- **Frontend Skill:**  
  - The consumer of these REST APIs.  
  - Backend must keep endpoint shapes and status codes stable so the Next.js frontend can rely on them.

---

## Usage Examples (for agents)

When the FastAPI Backend Agent wants to use this skill, it should issue prompts like:

> “Using **FastAPI Backend Skill**, implement all `/api/{user_id}/tasks` endpoints in `backend/app/routes/tasks.py` with full request/response validation, JWT-based auth using `BETTER_AUTH_SECRET`, and SQLModel CRUD operations against Neon, following `@specs/features/task-crud.md`, `@specs/features/authentication.md`, `@specs/api/rest-endpoints.md`, and `@specs/database/schema.md`.”

> “Using **FastAPI Backend Skill**, update the backend to support `status` and `sort` query parameters on `GET /api/{user_id}/tasks`, including validation (`422` on invalid values) and index-friendly queries on `tasks.user_id` and `tasks.completed`.”

Agents must **never** bypass this skill’s rules when writing or modifying backend code.
```markdown
# FastAPI Backend Skill – Complete Definition


**FastAPI Backend Skill** is a specialized capability focused on building and managing the **FastAPI backend REST API layer** for the Phase II Todo Full-Stack Web Application. When invoked, this skill provides expertise in REST API design, request/response validation, JWT authentication integration, SQLModel-based database interaction, error handling, and backend structuring for the hackathon todo application.[file:55][web:39][web:48][web:50][web:52]


---


## Table of Contents


1. [Skill Purpose](#skill-purpose)  
2. [Project-Specific Context](#project-specific-context)  
3. [Core Components](#core-components)  
   - [Route Design](#1-route-design)  
   - [Request Validation](#2-request-validation)  
   - [Response Modeling](#3-response-modeling)  
   - [JWT Authentication Integration](#4-jwt-authentication-integration)  
   - [Database Interaction](#5-database-interaction)  
   - [Error Handling](#6-error-handling)  
   - [Authorization & Ownership Rules](#7-authorization--ownership-rules)  
   - [Application Structure](#8-application-structure)  
   - [Performance & Pagination](#9-performance--pagination)  
   - [OpenAPI Documentation](#10-openapi-documentation)  
4. [When to Invoke FastAPI Backend Skill](#when-to-invoke-fastapi-backend-skill)  
5. [How FastAPI Backend Skill Works](#how-fastapi-backend-skill-works)  
6. [FastAPI Backend Skill Output](#fastapi-backend-skill-output)  
7. [Implementation Patterns](#implementation-patterns)  
8. [Phase II–Specific Rules](#phase-ii–specific-rules)  
9. [Troubleshooting Guide](#troubleshooting-guide)  


---


## Skill Purpose


FastAPI Backend Skill enables you to design, implement, and maintain the complete **backend HTTP API layer** for the hackathon todo application. It covers:


- REST API design (paths, methods, status codes)  
- Request validation using Pydantic/SQLModel models  
- Response modeling and serialization  
- JWT authentication integration (tokens from Better Auth)  
- User-based authorization and resource ownership rules  
- Database interaction via SQLModel sessions and models  
- Error handling with proper HTTP status codes  
- Backend project structure and best practices  
- Performance-aware query patterns for Neon-backed APIs  


This skill ensures a clean, secure, and spec-compliant backend that meets the **Phase II** project requirements and can be reused in later phases (chatbot, K8s, event-driven features).[file:55]


---


## Project-Specific Context


This skill operates within the **Phase II – Todo Full-Stack Web Application** scope.


### Technology Stack


| Layer        | Technology                    | Purpose                                           |
|-------------|-------------------------------|---------------------------------------------------|
| Backend     | FastAPI                       | HTTP server and routing framework                 |
| ORM         | SQLModel                      | ORM + data modeling for PostgreSQL                |
| Database    | Neon Serverless PostgreSQL    | Cloud-native Postgres for tasks data              |
| Auth Source | Better Auth (Next.js)         | Issues JWT tokens used by backend                 |
| Validation  | Pydantic / SQLModel models    | Request and response validation                   |[file:55][web:52]


### Backend Application Structure


```text
backend/
├── main.py              # FastAPI app entry point
├── database.py          # DB engine + get_session() dependency
├── models.py            # SQLModel models (Task, etc.)
├── auth.py              # JWT verification dependencies/middleware
├── routes/
│   ├── __init__.py
│   └── tasks.py         # Task-related API endpoints
├── schemas/
│   ├── __init__.py
│   └── task.py          # Pydantic/SQLModel request/response schemas
├── .env                 # Environment variables (DATABASE_URL, BETTER_AUTH_SECRET, etc.)
├── requirements.txt     # Python dependencies
└── README.md
```


### Backend Requirements from Spec


- Implement all **Basic Level** features as REST endpoints: Add, Delete, Update, View, Mark Complete.[file:55]  
- Use the following endpoints (user scoped):  
  - `GET    /api/{user_id}/tasks`  
  - `POST   /api/{user_id}/tasks`  
  - `GET    /api/{user_id}/tasks/{id}`  
  - `PUT    /api/{user_id}/tasks/{id}`  
  - `DELETE /api/{user_id}/tasks/{id}`  
  - `PATCH  /api/{user_id}/tasks/{id}/complete`[file:55]  
- All endpoints must require a valid JWT token in the `Authorization: Bearer <token>` header and must enforce user isolation.[file:55]


---


## Core Components


### 1. Route Design


#### Purpose

Design RESTful FastAPI routes that expose the todo operations required by the spec, with consistent URL patterns, methods, and status codes.[file:55]


#### Route Design Process


**Step 1: Identify Resources & Actions**

- Resource: `Task`  
- Actions (Phase II Basic Level):
  - Create (Add Task)
  - Read (View Task List + Task Detail)
  - Update (Update Task)
  - Delete (Delete Task)
  - Toggle completion (Mark as Complete)[file:55]


**Step 2: Define Endpoint Paths**

Using the Phase II spec’s user-scoped pattern: [file:55]

- `GET    /api/{user_id}/tasks`  
- `POST   /api/{user_id}/tasks`  
- `GET    /api/{user_id}/tasks/{id}`  
- `PUT    /api/{user_id}/tasks/{id}`  
- `DELETE /api/{user_id}/tasks/{id}`  
- `PATCH  /api/{user_id}/tasks/{id}/complete`  


**Step 3: Map HTTP Methods to Behavior**

| Method | Path                               | Behavior                      |
|--------|------------------------------------|-------------------------------|
| GET    | `/api/{user_id}/tasks`            | List tasks for user           |
| POST   | `/api/{user_id}/tasks`            | Create a new task             |
| GET    | `/api/{user_id}/tasks/{id}`       | Get single task               |
| PUT    | `/api/{user_id}/tasks/{id}`       | Replace/update task           |
| DELETE | `/api/{user_id}/tasks/{id}`       | Remove task                   |
| PATCH  | `/api/{user_id}/tasks/{id}/complete` | Toggle completion status  |


**Step 4: Implement Router**

```python
# routes/tasks.py
from fastapi import APIRouter, Depends, status
from typing import List

from schemas.task import TaskCreate, TaskRead, TaskUpdate
from auth import get_current_user
from database import get_session
from sqlmodel import Session

router = APIRouter(
    prefix="/api/{user_id}/tasks",
    tags=["tasks"]
)
```


**Step 5: Attach to main app**

```python
# main.py
from fastapi import FastAPI
from routes import tasks

app = FastAPI()
app.include_router(tasks.router)
```


**Route Design Best Practices**

- Use nouns for resources (`tasks`, not `doTask`).  
- Keep verbs in HTTP method choice, not in path.  
- Use path parameters for resource IDs, query parameters for filters/sorting.  
- Use meaningful tags for grouping in OpenAPI docs (`tags=["tasks"]`).[web:37]


---


### 2. Request Validation


#### Purpose

Validate all incoming data (body, path, query) using Pydantic/SQLModel models to guarantee the backend only processes well-formed requests.[web:39][web:50]


#### Validation Process


**Step 1: Define Request Schemas (`schemas/task.py`)**

```python
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
```


**Step 2: Validate Path & Query Parameters**

- Path:
  - `user_id: str`
  - `id: int`
- Query (if applicable, for filtering/sorting as spec evolves):
  - `status: Literal["all", "pending", "completed"]`
  - `sort: Literal["created", "title", "due_date"]`[file:55]


**Step 3: Use Schemas in Routes**

```python
@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(
    user_id: str,
    payload: TaskCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user),
):
    ...
```


**Validation Best Practices**

- Express domain rules (title length, description length) at schema level.  
- Prefer enums / Literal types for constrained strings (`status`, `sort`).  
- Let FastAPI/Pydantic generate 422 responses for invalid inputs automatically.[web:39][web:50]


---


### 3. Response Modeling


#### Purpose

Define explicit response schemas and ensure all responses conform to them, providing predictable and well-documented outputs.[web:48]


#### Response Model Design


**Step 1: Define TaskRead**

```python
class TaskRead(TaskBase):
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```


**Step 2: Use response_model in Endpoints**

```python
@router.get(
    "",
    response_model=list[TaskRead],
    summary="List all tasks for the authenticated user"
)
def list_tasks(...):
    ...
```


**Response Best Practices**

- Always set `response_model` on routes.  
- Return domain objects, not raw DB rows or ORM instances.  
- Hide internal/non-public fields (e.g. do not expose internal debug data).  
- Use appropriate status codes (200, 201, 204, etc.).[web:48]


---


### 4. JWT Authentication Integration


#### Purpose

Integrate JWT tokens issued by Better Auth so the backend can securely identify and authorize users without storing sessions.[file:55][web:51]


#### Token Expectations

- Tokens are issued by Better Auth at login.  
- Tokens contain at least:
  - `user_id` (string)
  - `email`
  - `exp` (expiry time).  
- Tokens are signed using `BETTER_AUTH_SECRET` shared between frontend and backend (from `.env`).[file:55]


#### Implementation Steps in `auth.py`


**Step 1: Extract Token**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
import os

security = HTTPBearer()
SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"
```


**Step 2: Define Current User Model**

```python
from pydantic import BaseModel

class CurrentUser(BaseModel):
    id: str
    email: str
```


**Step 3: Verify Token Dependency**

```python
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id: str = payload.get("user_id")
    email: str = payload.get("email")
    if not user_id or not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    return CurrentUser(id=user_id, email=email)
```


**Step 4: Enforce user_id Match in Routes**

```python
def ensure_user_owns_path(user_id: str, current_user: CurrentUser):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
```


**Auth Integration Best Practices**

- Never trust `user_id` from URL alone; always cross-check with token.  
- Return `401` for auth problems, `403` for ownership/permission issues.  
- Do not log raw tokens; log only claim summaries if needed.[web:48][web:51]


---


### 5. Database Interaction


#### Purpose

Use SQLModel sessions and models to perform all persistence operations, keeping business logic and queries inside the backend while respecting schema from the Database Skill.[file:55][web:52]


#### Session Management


**database.py**

```python
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

def get_session():
    with Session(engine) as session:
        yield session
```


#### CRUD Using SQLModel


**Create Task**

```python
from models import Task
from datetime import datetime

def create_task_for_user(session: Session, user_id: str, data: TaskCreate) -> Task:
    task = Task(
        user_id=user_id,
        title=data.title,
        description=data.description,
        completed=False,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```


**List Tasks**

```python
from sqlmodel import select

def list_tasks_for_user(session: Session, user_id: str, status_filter: str | None = None):
    stmt = select(Task).where(Task.user_id == user_id)

    if status_filter == "pending":
        stmt = stmt.where(Task.completed == False)
    elif status_filter == "completed":
        stmt = stmt.where(Task.completed == True)

    stmt = stmt.order_by(Task.created_at.desc())
    return session.exec(stmt).all()
```


**Update / Delete / Toggle** follow the same pattern: fetch by `(id, user_id)`, handle 404, modify, commit, refresh.


**DB Interaction Best Practices**

- Always scope queries by `user_id` to enforce isolation.[file:55]  
- Commit once per logical change; avoid unnecessary commits.  
- Wrap multi-step operations in try/except and roll back on error.  
- Never bypass SQLModel models with ad hoc raw SQL unless necessary.


---


### 6. Error Handling


#### Purpose

Provide consistent, secure, and user-friendly error responses from the backend API.[web:48]


#### Error Patterns


| Situation                        | Status | Behavior                                         |
|----------------------------------|--------|--------------------------------------------------|
| Missing/invalid JWT              | 401    | “Invalid or expired token”                       |
| Token user ≠ URL user_id         | 403    | “Forbidden”                                      |
| Task not found for this user     | 404    | “Task not found”                                 |
| Invalid query parameter          | 400    | “Invalid sort/status value”                      |
| Validation error (body/params)   | 422    | Auto-generated by FastAPI/Pydantic               |
| Unexpected server error          | 500    | Generic message, details only in logs            |


Use `HTTPException` with `status_code` and `detail` message:

```python
from fastapi import HTTPException, status

raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
```


**Error Handling Best Practices**

- Do not leak stack traces or DB errors to clients.  
- Return generic messages for security-sensitive failures.  
- Keep `detail` clear and high-level; log the low-level details server-side.[web:48]


---


### 7. Authorization & Ownership Rules


#### Purpose

Enforce that each user can only see and mutate their own tasks, as mandated by the spec.[file:55]


#### Ownership Rules

- Every task is associated with exactly one `user_id`.  
- All queries must be filtered by `current_user.id`.  
- If a task with given `id` does not belong to `current_user.id`, behave as “not found” or “forbidden” depending on the spec preference (404 is safer to avoid leaking IDs).


**Enforcement Pattern**

```python
def get_task_or_404(session: Session, user_id: str, task_id: int) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
```


---


### 8. Application Structure


#### Purpose

Keep the backend codebase clean, maintainable, and aligned with `backend/CLAUDE.md` and Spec-Kit conventions.[file:55][web:37]


#### Module Responsibilities

- `main.py` – App creation, router inclusion, global middleware (CORS, logging).  
- `database.py` – DB engine + `get_session`.  
- `models.py` – SQLModel DB models (reused by other agents).  
- `schemas/task.py` – Request/response schemas for tasks API.  
- `auth.py` – JWT verification & `get_current_user` dependency.  
- `routes/tasks.py` – All task endpoints and business logic wiring.


**Structure Best Practices**

- Keep route handlers short; delegate DB logic to helper functions or services.  
- Avoid circular imports by keeping clear layering (schemas/models → routes → main).  
- Use dependency injection for all cross-cutting concerns (auth, DB).


---


### 9. Performance & Pagination


#### Purpose

Ensure backend endpoints stay performant as the number of tasks grows.[web:52]


#### Patterns

- Use indexes (from Database Skill) in queries by filtering on indexed columns (`user_id`, `completed`, `created_at`).[file:55]  
- Add simple pagination when needed:
  - Query params: `limit`, `offset` or `page`, `page_size`
  - Always apply to list endpoints.

```python
def list_tasks_for_user(
    session: Session,
    user_id: str,
    limit: int = 50,
    offset: int = 0
):
    stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    stmt = stmt.offset(offset).limit(limit)
    return session.exec(stmt).all()
```


---


### 10. OpenAPI Documentation


#### Purpose

Leverage FastAPI’s automatic docs to produce clear, self-documenting APIs.[web:37]


#### Practices

- Use `summary` and `description` on route decorators.  
- Use tags (`tags=["tasks"]`) for grouping.  
- Write docstrings for models and dependencies.  
- Ensure schemas are well described (via `Field(description=...)`).


---


## When to Invoke FastAPI Backend Skill


Invoke this skill whenever you need to:

- Create or change FastAPI routes for the todo API.  
- Add validation rules for new fields or query parameters.  
- Integrate or adjust JWT auth behavior on backend.  
- Wire new database fields or tables into the API layer.  
- Improve error handling, status codes, or documentation.  
- Refactor backend structure while staying within the project conventions.


---


## How FastAPI Backend Skill Works


1. **Read specs:** Always consult `specs/features/task-crud.md`, `specs/features/authentication.md`, `specs/api/rest-endpoints.md`, and `specs/database/schema.md` before changing anything.[file:55]  
2. **Plan changes:** Determine which routes, schemas, and dependencies must be created or updated.  
3. **Update schemas:** Add/modify Pydantic/SQLModel models to reflect spec.  
4. **Update routes:** Implement or adjust FastAPI endpoints, injecting auth and DB dependencies.  
5. **Test behavior:** Ensure correct status codes, responses, and ownership enforcement.  
6. **Refine:** If behavior diverges from spec, update spec first, then implementation.


---


## FastAPI Backend Skill Output


When used correctly, this skill produces:

- Complete, spec-compliant FastAPI routes in `routes/tasks.py`.  
- Matching request/response schemas in `schemas/task.py`.  
- Working JWT-based auth integration in `auth.py`.  
- Correct SQLModel-based CRUD logic wired via `database.py` and `models.py`.  
- Clean error handling and consistent HTTP behavior.  
- Well-structured, documented backend ready for frontend and later AI/chatbot phases.


---

## Implementation Patterns


- Prefer **dependency injection** over global access (DB, auth).  
- Keep functions small and composable (e.g. `get_task_or_404`, `ensure_user_owns_path`).  
- Use **Spec-Driven Development**: never introduce new behavior without updating specs and tasks first.[file:55]


---


## Phase II–Specific Rules


- All task endpoints must require a valid JWT token.  
- Requests without a token must return `401 Unauthorized`.  
- Users must only see/modify their own tasks; this is enforced at every route.  
- Task model must match `specs/database/schema.md` for Phase II.  
- No manual code outside Claude Code / Spec-Kit loop in actual hackathon implementation.[file:55]


---


## Troubleshooting Guide


- **401 on every request**  
  - Check `BETTER_AUTH_SECRET` matches frontend.  
  - Verify Authorization header uses `Bearer <token>` format.  

- **403 even for correct user**  
  - Ensure `user_id` in URL equals `user_id` in token.  
  - Confirm you are not using email or another field.  

- **404 when task exists**  
  - Make sure your query filters by both `id` and `user_id`.  

- **422 validation errors**  
  - Check request body shape against `TaskCreate` / `TaskUpdate`.  
  - Verify field names and types match schemas.  

- **DB connection issues**  
  - Verify `DATABASE_URL` is Neon’s connection string.  
  - Ensure SSL and pooling options are configured correctly.  

Using these patterns, the FastAPI Backend Skill ensures a robust, secure, and spec-aligned backend for your todo application.
```