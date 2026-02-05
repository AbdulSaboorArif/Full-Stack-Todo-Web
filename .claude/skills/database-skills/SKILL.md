```markdown
# Database Skill - Complete Definition

**Database Skill** is a specialized capability focused on managing Neon Serverless PostgreSQL operations for the Phase II Todo Full-Stack Web Application. When invoked, this skill provides expertise in database schema design, SQLModel ORM implementation, migrations, CRUD operations, query optimization, and data integrity for the hackathon todo application.

---

## Table of Contents

1. [Skill Purpose](#skill-purpose)
2. [Project-Specific Context](#project-specific-context)
3. [Core Components](#core-components)
   - [Schema Design](#1-schema-design)
   - [Table Creation](#2-table-creation)
   - [Migrations](#3-migrations)
   - [Relationships](#4-relationships)
   - [SQLModel Models](#5-sqlmodel-models)
   - [CRUD Operations](#6-crud-operations)
   - [Query Optimization](#7-query-optimization)
   - [Data Constraints](#8-data-constraints)
   - [Transactions](#9-transactions)
   - [Connection Management](#10-connection-management)
4. [When to Invoke Database Skill](#when-to-invoke-database-skill)
5. [How Database Skill Works](#how-database-skill-works)
6. [Database Skill Output](#database-skill-output)
7. [Implementation Patterns](#implementation-patterns)
8. [Neon Serverless Best Practices](#neon-serverless-best-practices)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## Skill Purpose

Database Skill enables you to design, implement, and manage the complete database layer for the hackathon todo application. It covers:

- Database schema design and normalization
- Table creation with proper constraints
- SQLModel ORM model implementation
- Database migrations and versioning
- Establishing relationships (foreign keys)
- CRUD (Create, Read, Update, Delete) operations
- Query optimization with indexes
- Data integrity enforcement
- Transaction management
- Connection pooling and session handling
- Neon Serverless PostgreSQL optimization

This skill ensures efficient, scalable, and data-integrity-focused database solutions that follow industry best practices and meet the Phase II project requirements.

---

## Project-Specific Context

This skill operates within the Phase II requirements:

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Database | Neon Serverless PostgreSQL | Cloud-native PostgreSQL database |
| ORM | SQLModel | Python ORM combining SQLAlchemy + Pydantic |
| Backend | FastAPI | Web framework using the ORM |
| Migrations | SQLModel.metadata.create_all() | Initial setup (Alembic for production) |
| Connection | psycopg2 | PostgreSQL adapter |

### Database Architecture

**Database Service:** Neon Serverless PostgreSQL
- Cloud-hosted PostgreSQL
- Serverless architecture (auto-scaling)
- Branching capability for dev/staging
- Automatic backups
- Point-in-time recovery
- Connection pooling required
- SSL/TLS encryption

**ORM Layer:** SQLModel
- Combines SQLAlchemy (database) + Pydantic (validation)
- Type-safe database models
- Automatic schema generation
- Query builder with type hints
- Validation at model level

**Application Layer:** FastAPI
- Uses SQLModel models
- Dependency injection for sessions
- Async/sync support
- RESTful API endpoints

### Database Requirements for Todo App

#### Tables to Manage

**1. users table (managed by Better Auth)**
- You reference this table but don't create it
- Better Auth creates and manages it
- Your tasks table has foreign key to users

**Schema Reference:**
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**2. tasks table (you create and manage)**

**Requirements:**
- id: integer, primary key, auto-increment
- user_id: string (foreign key → users.id)
- title: string, required, 1-200 characters
- description: text, optional, max 1000 characters
- completed: boolean, default false
- created_at: timestamp, default current time
- updated_at: timestamp, default current time

**Schema:**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Required Indexes

**Purpose:** Speed up common queries

**Indexes to Create:**
1. **tasks.user_id** - For filtering tasks by user
   - Query: `SELECT * FROM tasks WHERE user_id = ?`
   - Most common query in the app

2. **tasks.completed** - For filtering by status
   - Query: `SELECT * FROM tasks WHERE completed = ?`
   - Used for "show only pending" or "show only completed"

3. **tasks (user_id, completed)** - Composite index
   - Query: `SELECT * FROM tasks WHERE user_id = ? AND completed = ?`
   - Combines both filters efficiently

4. **tasks.created_at** - For sorting by date
   - Query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
   - Used for showing newest tasks first

#### Data Integrity Rules

**Constraints:**
- user_id is NOT NULL (every task must have an owner)
- title is NOT NULL (every task needs a title)
- title length between 1-200 characters
- description max 1000 characters
- completed defaults to false
- Foreign key: user_id → users.id
- Cascade delete: when user deleted, delete their tasks

**Validation:**
- Title cannot be empty string
- Title cannot exceed 200 characters
- Description cannot exceed 1000 characters
- user_id must reference existing user
- completed must be boolean

**Business Rules:**
- User can only access their own tasks
- Task must belong to exactly one user
- Task cannot exist without user
- created_at cannot be changed
- updated_at changes on every update

---

## Core Components

### 1. Schema Design

#### Purpose
Design normalized, efficient database schemas that model the application's data requirements while ensuring data integrity and query performance.

#### Schema Design Process

**Step 1: Identify Entities**
- What "things" does the application track?
- For todo app: User, Task
- User managed by Better Auth
- Task managed by you

**Step 2: Define Attributes**
- What properties does each entity have?
- User: id, email, name, created_at
- Task: id, user_id, title, description, completed, created_at, updated_at

**Step 3: Determine Relationships**
- How do entities relate to each other?
- One User has Many Tasks (one-to-many)
- One Task belongs to One User (many-to-one)
- Relationship: User ←→ Tasks

**Step 4: Choose Data Types**

**PostgreSQL Data Types for Todo App:**

| Field | PostgreSQL Type | Reason |
|-------|----------------|---------|
| id (tasks) | SERIAL (INTEGER) | Auto-incrementing primary key |
| id (users) | VARCHAR(255) | Better Auth uses string IDs |
| user_id | VARCHAR(255) | Matches users.id type |
| email | VARCHAR(255) | Standard email max length |
| name | VARCHAR(100) | Sufficient for names |
| title | VARCHAR(200) | Project requirement: max 200 |
| description | TEXT | Variable length, up to 1000 chars |
| completed | BOOLEAN | True/false value |
| created_at | TIMESTAMP | Date and time of creation |
| updated_at | TIMESTAMP | Date and time of last update |

**Data Type Guidelines:**
- Use SERIAL for auto-incrementing IDs
- Use VARCHAR(n) for limited-length strings
- Use TEXT for variable-length strings
- Use BOOLEAN for true/false flags
- Use TIMESTAMP for date/time values
- Use INTEGER for whole numbers
- Use NUMERIC for decimal numbers

**Step 5: Define Primary Keys**
- Unique identifier for each record
- tasks.id: Primary key (SERIAL)
- users.id: Primary key (VARCHAR)

**Step 6: Define Foreign Keys**
- Links between tables
- tasks.user_id REFERENCES users.id
- Ensures referential integrity
- Cascade delete: when user deleted, tasks deleted

**Step 7: Plan Indexes**
- Speed up common queries
- Index columns used in WHERE clauses
- Index columns used in JOIN conditions
- Index columns used in ORDER BY

**Step 8: Set Constraints**
- NOT NULL: Required fields
- UNIQUE: No duplicates
- CHECK: Value validation
- DEFAULT: Default values
- FOREIGN KEY: Referential integrity

#### Normalization

**What is Normalization?**
- Process of organizing data to reduce redundancy
- Eliminates duplicate data
- Ensures data integrity
- Improves query efficiency

**Normal Forms:**

**1st Normal Form (1NF):**
- Each column contains atomic values
- No repeating groups
- Each row is unique

**2nd Normal Form (2NF):**
- Must be in 1NF
- No partial dependencies
- All attributes depend on entire primary key

**3rd Normal Form (3NF):**
- Must be in 2NF
- No transitive dependencies
- All attributes depend only on primary key

**Todo App Normalization:**
```
Users Table:
- id (PK)
- email
- name
- created_at

Tasks Table:
- id (PK)
- user_id (FK → users.id)
- title
- description
- completed
- created_at
- updated_at

✅ No redundant data
✅ Each table has single purpose
✅ Relationships via foreign keys
✅ Normalized to 3NF
```

#### Schema Design Best Practices

**Naming Conventions:**
- Table names: lowercase, plural (users, tasks)
- Column names: lowercase, snake_case (user_id, created_at)
- Primary keys: id
- Foreign keys: {table}_id (user_id)
- Boolean columns: is_* or past tense (completed, is_active)
- Timestamps: *_at (created_at, updated_at)

**Data Integrity:**
- Always define primary keys
- Use foreign keys for relationships
- Add NOT NULL for required fields
- Set appropriate DEFAULT values
- Use CHECK constraints for validation
- Create UNIQUE constraints where needed

**Performance:**
- Index foreign key columns
- Index columns in WHERE clauses
- Create composite indexes for multi-column queries
- Don't over-index (slows inserts/updates)
- Keep tables normalized

**Scalability:**
- Plan for growth
- Use appropriate data types
- Consider partitioning for large tables
- Design for query patterns
- Avoid premature optimization

---

### 2. Table Creation

#### Purpose
Create database tables with proper structure, constraints, and indexes to store application data.

#### Table Creation Methods

**Method 1: SQLModel Automatic (Recommended for Phase II)**
```python
from sqlmodel import SQLModel, create_engine

# Define models (shown in section 5)
# Then create all tables
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

**Method 2: Manual SQL**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Method 3: Alembic Migrations (Production)**
```bash
alembic revision --autogenerate -m "Create tasks table"
alembic upgrade head
```

#### Creating tasks Table with SQLModel

**Step 1: Define Task Model**
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Step 2: Create Database Connection**
```python
from sqlmodel import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (dev only)
    pool_pre_ping=True,  # Verify connections
    pool_size=10,  # Connection pool size
    max_overflow=20  # Max connections above pool_size
)
```

**Step 3: Create Tables**
```python
def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)
```

**Step 4: Call on Application Startup**
```python
# In main.py
from fastapi import FastAPI
from database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db()
```

#### Adding Indexes

**Single Column Index:**
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Creates index
    completed: bool = Field(default=False, index=True)  # Creates index
```

**Composite Index (Multiple Columns):**
```python
from sqlalchemy import Index

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        Index('idx_user_completed', 'user_id', 'completed'),
        Index('idx_user_created', 'user_id', 'created_at'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Table Creation Best Practices

**Primary Keys:**
- Every table must have a primary key
- Use SERIAL (auto-increment) for integer IDs
- Use UUID for distributed systems
- Name it 'id' for consistency

**Foreign Keys:**
- Always define foreign key relationships
- Use ON DELETE CASCADE for dependent data
- Use ON DELETE SET NULL for optional relationships
- Index all foreign key columns

**Default Values:**
- Set defaults for optional fields
- Use database defaults (DEFAULT clause)
- Use application defaults (Field(default=...))
- Timestamps: use CURRENT_TIMESTAMP or datetime.utcnow

**NOT NULL Constraints:**
- Mark required fields as NOT NULL
- In SQLModel: don't use Optional[]
- Prevents incomplete data
- Enforced at database level

**String Lengths:**
- Always specify max length for VARCHAR
- Use TEXT for unlimited length
- Consider storage implications
- Match business requirements

---

### 3. Migrations

#### Purpose
Manage database schema changes over time, allowing evolution of the database structure without data loss.

#### What Are Migrations?

**Definition:**
- Scripts that modify database schema
- Version-controlled changes
- Applied sequentially
- Reversible (rollback capability)
- Track database evolution

**Why Migrations?**
- Track schema changes in version control
- Apply changes consistently across environments
- Collaborate on schema changes
- Roll back problematic changes
- Document database evolution

#### Migration Strategies for Phase II

**Initial Setup (Development):**
```python
# Use SQLModel.metadata.create_all()
# Simple, fast, good for development
# Not suitable for production with existing data

from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)

def init_db():
    """Create all tables from SQLModel models"""
    SQLModel.metadata.create_all(engine)
```

**When to Use:**
- First time setting up database
- Development environment
- Testing
- Fresh deployments

**What It Does:**
- Reads all SQLModel model definitions
- Generates CREATE TABLE statements
- Creates tables if they don't exist
- Does NOT modify existing tables
- Does NOT delete tables

#### Schema Changes After Initial Setup

**Scenario:** Need to add new column to tasks table

**Option 1: Manual SQL (Quick but Risky)**
```sql
ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 1;
```

**Problems:**
- Not version controlled
- Manual application on each environment
- No rollback capability
- Easy to forget in production

**Option 2: Alembic Migrations (Recommended for Production)**

**Step 1: Install Alembic**
```bash
pip install alembic
```

**Step 2: Initialize Alembic**
```bash
alembic init alembic
```

**Step 3: Configure Alembic**
```python
# alembic/env.py
from sqlmodel import SQLModel
from models import Task  # Import all models

target_metadata = SQLModel.metadata
```

**Step 4: Generate Migration**
```bash
alembic revision --autogenerate -m "Add priority column to tasks"
```

**Step 5: Review Migration**
```python
# alembic/versions/xxxx_add_priority.py
def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.Integer(), default=1))

def downgrade():
    op.drop_column('tasks', 'priority')
```

**Step 6: Apply Migration**
```bash
alembic upgrade head
```

**Step 7: Rollback if Needed**
```bash
alembic downgrade -1  # Go back one migration
```

#### Common Migration Scenarios

**Add Column with Default:**
```python
# Update model
class Task(SQLModel, table=True):
    priority: int = Field(default=1)

# Generate migration
# alembic revision --autogenerate -m "Add priority"

# Migration creates:
def upgrade():
    op.add_column('tasks',
        sa.Column('priority', sa.Integer(), server_default='1')
    )
```

**Remove Column:**
```python
# Remove from model
# class Task(SQLModel, table=True):
#     # Remove: priority: int = Field(default=1)

# Generate migration
# Migration creates:
def upgrade():
    op.drop_column('tasks', 'priority')

def downgrade():
    op.add_column('tasks', sa.Column('priority', sa.Integer()))
```

**Rename Column:**
```python
# Migration:
def upgrade():
    op.alter_column('tasks', 'description', new_column_name='details')

def downgrade():
    op.alter_column('tasks', 'details', new_column_name='description')
```

**Add Index:**
```python
def upgrade():
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])

def downgrade():
    op.drop_index('idx_tasks_priority', 'tasks')
```

**Change Column Type:**
```python
def upgrade():
    # Must be careful with data migration
    op.alter_column('tasks', 'priority',
        type_=sa.String(),
        postgresql_using='priority::text'
    )
```

#### Migration Best Practices

**Before Creating Migration:**
- Backup database
- Test on development database first
- Review auto-generated migrations
- Add data migrations if needed
- Plan for rollback

**Migration Guidelines:**
- One logical change per migration
- Include both upgrade and downgrade
- Test rollback works
- Document complex migrations
- Keep migrations small and focused

**Data Migrations:**
```python
def upgrade():
    # 1. Add new column
    op.add_column('tasks', sa.Column('priority', sa.Integer()))
    
    # 2. Migrate data
    connection = op.get_bind()
    connection.execute(
        "UPDATE tasks SET priority = 1 WHERE priority IS NULL"
    )
    
    # 3. Make column NOT NULL
    op.alter_column('tasks', 'priority', nullable=False)
```

**Testing Migrations:**
```bash
# Apply migration
alembic upgrade head

# Test application works

# Rollback
alembic downgrade -1

# Test application still works

# Re-apply
alembic upgrade head
```

#### Phase II Migration Strategy

**For Hackathon/Development:**
```python
# Use SQLModel.metadata.create_all()
# Fast iteration
# Easy to reset database
# Good for hackathon pace

# database.py
def init_db():
    SQLModel.metadata.create_all(engine)

# main.py
@app.on_event("startup")
async def startup():
    init_db()
```

**For Production Later:**
```bash
# Switch to Alembic
# Install: pip install alembic
# Initialize: alembic init alembic
# Generate: alembic revision --autogenerate
# Apply: alembic upgrade head
```

---

### 4. Relationships

#### Purpose
Define how tables relate to each other through foreign keys, enabling efficient data retrieval and maintaining referential integrity.

#### Relationship Types

**One-to-Many (Most Common):**
- One User has Many Tasks
- One Task belongs to One User
- Foreign key in "many" side (tasks.user_id)

**Many-to-Many:**
- Many Students attend Many Courses
- Requires junction table
- Not needed for Phase II

**One-to-One:**
- One User has One Profile
- Foreign key with UNIQUE constraint
- Not needed for Phase II

#### User-Task Relationship

**Relationship:** User ←→ Tasks (One-to-Many)

```
┌─────────────┐
│   users     │
├─────────────┤
│ id (PK)     │◄──┐
│ email       │   │
│ name        │   │
│ created_at  │   │
└─────────────┘   │
                  │
                  │ ONE user
                  │ has
                  │ MANY tasks
                  │
┌─────────────┐   │
│   tasks     │   │
├─────────────┤   │
│ id (PK)     │   │
│ user_id (FK)│───┘
│ title       │
│ description │
│ completed   │
│ created_at  │
│ updated_at  │
└─────────────┘
```

#### Defining Foreign Keys

**In SQLModel:**
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    
    # Relationship (ORM navigation)
    tasks: List["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Foreign key
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    
    # Relationship (ORM navigation)
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Foreign Key Components:**
- **foreign_key="users.id"**: Points to users table, id column
- **index=True**: Creates index for faster queries
- **Relationship()**: ORM navigation (Python-level, not database)

#### Cascade Behavior

**What is CASCADE?**
- Defines what happens when referenced row is deleted
- Maintains referential integrity
- Prevents orphaned records

**CASCADE Options:**

**ON DELETE CASCADE:**
- When user deleted, delete all their tasks
- Recommended for Phase II
- Prevents orphaned tasks

```sql
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

**ON DELETE SET NULL:**
- When user deleted, set task.user_id to NULL
- Task remains but loses owner
- Not suitable for todo app (tasks need owner)

**ON DELETE RESTRICT:**
- Prevent deleting user if they have tasks
- Must delete tasks first
- More manual control

**ON DELETE NO ACTION:**
- Default behavior
- Similar to RESTRICT
- May defer constraint check

**SQLModel Implementation:**
```python
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Method 1: Using Field (simpler)
    user_id: str = Field(foreign_key="users.id")
    
    # Method 2: Using sa_column (more control)
    user_id: str = Field(
        sa_column=Column(
            "user_id",
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
```

#### Relationship Navigation (ORM)

**What is Relationship()?**
- Python-level navigation between models
- Not a database construct
- Allows accessing related objects
- Lazy or eager loading

**Using Relationships:**
```python
from sqlmodel import Session, select

# Get user with their tasks
user = session.get(User, "user_123")

# Access tasks through relationship
user_tasks = user.tasks  # List of Task objects
for task in user_tasks:
    print(task.title)

# Access user from task
task = session.get(Task, 1)
task_owner = task.user  # User object
print(task_owner.email)
```

**Benefits:**
- Cleaner code (no manual joins)
- Type safety
- Automatic query generation
- Prevents N+1 query problems (with eager loading)

#### Querying Related Data

**Get Tasks for a User:**
```python
def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    # Method 1: Using relationship
    user = session.get(User, user_id)
    return user.tasks
    
    # Method 2: Using query (more common)
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks
```

**Get User from Task:**
```python
def get_task_owner(session: Session, task_id: int) -> User:
    # Method 1: Using relationship
    task = session.get(Task, task_id)
    return task.user
    
    # Method 2: Using join
    statement = select(User).join(Task).where(Task.id == task_id)
    user = session.exec(statement).first()
    return user
```

**Eager Loading (Prevent N+1 Queries):**
```python
from sqlmodel import select
from sqlalchemy.orm import selectinload

# Load user with all tasks in one query
statement = select(User).options(selectinload(User.tasks)).where(User.id == user_id)
user = session.exec(statement).first()

# Now accessing user.tasks doesn't trigger additional query
for task in user.tasks:
    print(task.title)  # No extra query
```

#### Relationship Best Practices

**Foreign Key Indexes:**
- Always index foreign key columns
- Dramatically improves join performance
- Essential for WHERE clauses on foreign keys

**Naming Conventions:**
- Foreign key: {table}_id (user_id)
- Relationship attribute: plural for many (tasks)
- Relationship attribute: singular for one (user)

**Cascade Decisions:**
- Dependent data: ON DELETE CASCADE
- Optional relationships: ON DELETE SET NULL
- Protected relationships: ON DELETE RESTRICT
- Todo app: CASCADE (tasks depend on users)

**Referential Integrity:**
- Always define foreign keys
- Enforced at database level
- Prevents orphaned records
- Ensures data consistency

---

### 5. SQLModel Models

#### Purpose
Define Python classes that map to database tables, combining SQLAlchemy's ORM capabilities with Pydantic's validation.

#### What is SQLModel?

**SQLModel = SQLAlchemy + Pydantic**
- **SQLAlchemy**: Python ORM for databases
- **Pydantic**: Data validation using Python type hints
- **SQLModel**: Best of both worlds

**Benefits:**
- Type-safe database models
- Automatic validation
- Editor autocomplete
- FastAPI integration
- Single model for DB and API

#### Task Model Implementation

**Complete Task Model:**
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from sqlalchemy import Index

class Task(SQLModel, table=True):
    """
    Task model representing a todo item
    
    Attributes:
        id: Auto-incrementing primary key
        user_id: Foreign key to users table
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 chars)
        completed: Task completion status
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = "tasks"
    
    # Define composite indexes
    __table_args__ = (
        Index('idx_user_completed', 'user_id', 'completed'),
        Index('idx_user_created', 'user_id', 'created_at'),
    )
    
    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier"
    )
    
    # Foreign key to users
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="ID of user who owns this task"
    )
    
    # Task data
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title"
    )
    
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )
    
    completed: bool = Field(
        default=False,
        index=True,
        description="Task completion status"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was created"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was last updated"
    )
    
    # Relationship to User (ORM navigation)
    user: Optional["User"] = Relationship(back_populates="tasks")
```

#### Field Configuration

**Field() Parameters:**

**Data Validation:**
- `min_length`: Minimum string length
- `max_length`: Maximum string length
- `ge`: Greater than or equal (numbers)
- `le`: Less than or equal (numbers)
- `gt`: Greater than (numbers)
- `lt`: Less than (numbers)
- `regex`: Regex pattern matching

**Database Configuration:**
- `primary_key`: Marks as primary key
- `foreign_key`: References another table
- `index`: Creates database index
- `unique`: Ensures uniqueness
- `nullable`: Allows NULL values

**Default Values:**
- `default`: Static default value
- `default_factory`: Function that returns default
- `server_default`: Database-level default (SQL)

**Metadata:**
- `description`: Field documentation
- `title`: Field title
- `alias`: Alternative field name

**Examples:**
```python
# Auto-increment ID
id: Optional[int] = Field(default=None, primary_key=True)

# Required field with length limit
title: str = Field(min_length=1, max_length=200)

# Optional field with max length
description: Optional[str] = Field(default=None, max_length=1000)

# Boolean with default
completed: bool = Field(default=False)

# Timestamp with function default
created_at: datetime = Field(default_factory=datetime.utcnow)

# Foreign key with index
user_id: str = Field(foreign_key="users.id", index=True)

# Unique email
email: str = Field(unique=True, index=True)

