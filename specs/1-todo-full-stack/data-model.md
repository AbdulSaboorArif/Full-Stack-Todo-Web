---
# Data Model: Todo Full-Stack Web Application

**Branch**: `1-todo-full-stack` | **Date**: 2026-02-03 | **Spec**: `specs/1-todo-full-stack/spec.md`
**Input**: Feature specification from `/specs/1-todo-full-stack/spec.md`

## Entity Definitions

### User Entity

**Purpose**: Represents an authenticated user with email, password, and unique identifier

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Fields**:
- `id`: SERIAL PRIMARY KEY - Auto-incrementing unique identifier
- `email`: VARCHAR(255) UNIQUE NOT NULL - User's email address (used for login)
- `password_hash`: VARCHAR(255) NOT NULL - Hashed password for authentication
- `created_at`: TIMESTAMP WITH TIME ZONE - Record creation timestamp
- `updated_at`: TIMESTAMP WITH TIME ZONE - Last update timestamp

**Validation Rules**:
- Email must be unique across all users
- Email format must be valid
- Password must meet complexity requirements (handled by Better Auth)
- Email length limited to 255 characters

### Task Entity

**Purpose**: Represents a user task with title, description, completion status, creation date, and association to a user

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,

    UNIQUE(user_id, id)
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed_at ON tasks(completed_at) WHERE completed_at IS NOT NULL;
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
```

**Fields**:
- `id`: SERIAL PRIMARY KEY - Auto-incrementing unique identifier
- `user_id`: INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE - Foreign key to user
- `title`: VARCHAR(255) NOT NULL - Task title (required)
- `description`: TEXT - Optional task description
- `is_completed`: BOOLEAN DEFAULT FALSE - Completion status
- `created_at`: TIMESTAMP WITH TIME ZONE - Record creation timestamp
- `updated_at`: TIMESTAMP WITH TIME ZONE - Last update timestamp
- `completed_at`: TIMESTAMP WITH TIME ZONE - Completion timestamp (null if incomplete)

**Validation Rules**:
- Title is required and limited to 255 characters
- User ID must reference an existing user
- is_completed defaults to FALSE
- completed_at is set when task is marked complete

**State Transitions**:
- **New Task**: `is_completed = FALSE`, `completed_at = NULL`
- **Mark Complete**: `is_completed = TRUE`, `completed_at = CURRENT_TIMESTAMP`
- **Mark Incomplete**: `is_completed = FALSE`, `completed_at = NULL`
- **Update**: `updated_at = CURRENT_TIMESTAMP`

## Relationships

### User ↔ Task (One-to-Many)
- One user can have many tasks
- Each task belongs to exactly one user
- Foreign key constraint with ON DELETE CASCADE
- User isolation enforced through user_id filtering

## Database Constraints

### Referential Integrity
- `tasks.user_id` references `users.id` with ON DELETE CASCADE
- Deleting a user automatically deletes their tasks

### Uniqueness Constraints
- `users.email` must be unique
- Combination of `user_id` and `id` ensures unique task identifiers per user

### Index Strategy
- `idx_tasks_user_id`: Optimizes user-specific task queries
- `idx_tasks_completed_at`: Optimizes queries for completed tasks
- `idx_tasks_is_completed`: Optimizes filtering by completion status

## SQLModel Implementation

### User Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from .user import User

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="User.id", index=True)
    title: str
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(onupdate=datetime.utcnow, default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationship to User
    user: Optional[User] = Relationship()
```

## Migration Strategy

### Initial Migration
1. Create users table
2. Create tasks table with foreign key
3. Add indexes for performance

### Future Migrations
- Add task priority field
- Add task due dates
- Add task categories/tags
- Add user profile information

## Data Validation Rules

### User Validation
- Email format validation
- Password complexity validation (handled by Better Auth)
- Unique email constraint

### Task Validation
- Title required (max 255 characters)
- Description optional (no length limit)
- User ID must reference existing user
- State transitions must be valid

---

*Data model complete. All entities, relationships, and constraints defined.*