```markdown
# Debugging Skill - Complete Definition

**Debugging Skill** is a specialized capability focused on identifying, diagnosing, and resolving errors in the Phase II Todo Full-Stack Web Application. When invoked, this skill provides expertise in error analysis, root cause identification, systematic troubleshooting, and implementing verified solutions across all layers of the application stack.

---

## Table of Contents

1. [Skill Purpose](#skill-purpose)
2. [Project-Specific Context](#project-specific-context)
3. [Core Components](#core-components)
   - [Error Analysis](#1-error-analysis)
   - [Root Cause Identification](#2-root-cause-identification)
   - [Systematic Troubleshooting](#3-systematic-troubleshooting)
   - [Solution Implementation](#4-solution-implementation)
   - [Verification & Testing](#5-verification--testing)
   - [Dependency Management](#6-dependency-management)
   - [Configuration Debugging](#7-configuration-debugging)
   - [Database Debugging](#8-database-debugging)
   - [API Debugging](#9-api-debugging)
   - [Authentication Debugging](#10-authentication-debugging)
4. [When to Invoke Debugging Skill](#when-to-invoke-debugging-skill)
5. [How Debugging Skill Works](#how-debugging-skill-works)
6. [Debugging Skill Output](#debugging-skill-output)
7. [Debugging Patterns](#debugging-patterns)
8. [Error Categories](#error-categories)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## Skill Purpose

Debugging Skill enables you to systematically identify and resolve errors across the entire todo application stack. It covers:

- Reading and interpreting error messages and stack traces
- Identifying error types and categories
- Diagnosing root causes through systematic analysis
- Implementing verified solutions
- Testing fixes thoroughly
- Preventing similar errors in the future
- Debugging frontend issues (React, Next.js, Better Auth)
- Debugging backend issues (FastAPI, SQLModel, JWT)
- Debugging database issues (PostgreSQL, connections, queries)
- Debugging integration issues (CORS, authentication flow)

This skill ensures rapid error resolution, minimizes debugging time, and maintains application stability throughout development.

---

## Project-Specific Context

This skill operates within the Phase II requirements:

### Technology Stack to Debug

| Layer | Technology | Common Error Types |
|-------|-----------|-------------------|
| **Frontend** | Next.js 16 + React | Build errors, component errors, hydration mismatches |
| **Styling** | Tailwind CSS | Class conflicts, purge issues, missing utilities |
| **Auth (Frontend)** | Better Auth | Configuration errors, session issues, token problems |
| **Backend** | FastAPI | Import errors, dependency issues, route errors |
| **ORM** | SQLModel | Model errors, relationship issues, query errors |
| **Database** | Neon PostgreSQL | Connection failures, migration errors, constraint violations |
| **Auth (Backend)** | PyJWT | Token verification failures, signature mismatches |
| **Integration** | CORS, HTTP | CORS errors, 401/403 errors, network failures |

### Error Context

**Development Environment:**
- Frontend runs on http://localhost:3000
- Backend runs on http://localhost:8000
- Database hosted on Neon (cloud PostgreSQL)
- Two separate codebases (frontend/, backend/)
- Shared authentication secret (BETTER_AUTH_SECRET)

**Common Error Sources:**
- Environment variable mismatches
- CORS misconfiguration
- Database connection issues
- JWT token verification failures
- Missing dependencies
- Import/export errors
- Type mismatches
- Async/await issues

---

## Core Components

### 1. Error Analysis

#### Purpose
Read and interpret error messages, stack traces, and console output to understand what went wrong and where.

#### Error Message Anatomy

**Example Error Message:**
```
Traceback (most recent call last):
  File "/app/backend/main.py", line 5, in <module>
    from models import Task
  File "/app/backend/models.py", line 3, in <module>
    from database import engine
  File "/app/backend/database.py", line 15, in <module>
    engine = create_engine(DATABASE_URL)
  File "/venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 518, in create_engine
    raise exc.ArgumentError("Could not parse SQLAlchemy URL from string")
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from string
```

**Breaking Down the Error:**

1. **Error Type:** `sqlalchemy.exc.ArgumentError`
   - Library: SQLAlchemy
   - Category: Argument/Input Error
   - Specific: URL parsing error

2. **Error Message:** `"Could not parse SQLAlchemy URL from string"`
   - Problem: Invalid or missing database URL
   - Cause: DATABASE_URL format is incorrect or empty

3. **Stack Trace (Read Bottom to Top):**
   - **Bottom (Root Cause):** SQLAlchemy's `create_engine()` can't parse URL
   - **Middle:** Called from `database.py` line 15
   - **Top (Entry Point):** Started in `main.py` importing models

4. **File Locations:**
   - `/app/backend/database.py` line 15: Where error occurred
   - `/app/backend/models.py` line 3: Importing database
   - `/app/backend/main.py` line 5: Initial import

**Reading Stack Traces:**

**Rule: Read from Bottom to Top**
```
main.py (imports) → models.py (imports) → database.py (ERROR HERE)
                                             ↑
                                      Fix this file!
```

**What to Extract:**
- **File path:** Where error occurred
- **Line number:** Exact location
- **Function name:** What was being called
- **Error type:** Category of error
- **Error message:** Specific problem description

#### Error Message Patterns

**Pattern 1: Missing Module**
```
ModuleNotFoundError: No module named 'fastapi'
```
- **Type:** Import Error
- **Cause:** Package not installed
- **Solution:** Install package with pip

**Pattern 2: Import Name Error**
```
ImportError: cannot import name 'Field' from 'sqlmodel'
```
- **Type:** Import Error
- **Cause:** Wrong import, typo, or version mismatch
- **Solution:** Check import statement and package version

**Pattern 3: Database Connection**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```
- **Type:** Connection Error
- **Cause:** Database unreachable, wrong URL, or credentials
- **Solution:** Check DATABASE_URL and network connectivity

**Pattern 4: Authentication Error**
```
jwt.exceptions.InvalidSignatureError: Signature verification failed
```
- **Type:** JWT Error
- **Cause:** Secret mismatch between frontend and backend
- **Solution:** Verify BETTER_AUTH_SECRET is identical

**Pattern 5: Validation Error**
```
pydantic.error_wrappers.ValidationError: 1 validation error for Task
title
  field required (type=value_error.missing)
```
- **Type:** Validation Error
- **Cause:** Missing required field in request
- **Solution:** Ensure frontend sends all required fields

**Pattern 6: Type Error**
```
TypeError: 'NoneType' object is not iterable
```
- **Type:** Runtime Error
- **Cause:** Trying to iterate over None (expected list/array)
- **Solution:** Check for None before iterating, handle empty results

**Pattern 7: CORS Error (Browser Console)**
```
Access to fetch at 'http://localhost:8000/api/1/tasks' from origin 'http://localhost:3000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```
- **Type:** CORS Error
- **Cause:** Backend not configured to allow frontend origin
- **Solution:** Add CORS middleware to FastAPI

#### Browser Console Analysis

**Frontend Errors Appear in Browser Console (F12)**

**Example Console Error:**
```javascript
Error: Request failed with status code 401
    at createError (createError.js:16)
    at settle (settle.js:17)
    at XMLHttpRequest.handleLoad (xhr.js:62)
```

**Console Error Types:**

**Network Errors:**
```
Failed to load resource: the server responded with a status of 404 (Not Found)
```
- **Meaning:** API endpoint doesn't exist
- **Check:** Backend route definition

**CORS Errors:**
```
has been blocked by CORS policy
```
- **Meaning:** Backend not allowing frontend requests
- **Check:** CORS middleware configuration

**React Errors:**
```
Uncaught Error: Rendered fewer hooks than expected
```
- **Meaning:** Hook rules violated
- **Check:** Conditional hook usage

**Hydration Errors (Next.js):**
```
Hydration failed because the initial UI does not match what was rendered on the server
```
- **Meaning:** Server HTML doesn't match client HTML
- **Check:** Dynamic content, useEffect usage

#### Log Analysis

**Backend Logs (Terminal Running uvicorn):**
```
INFO:     127.0.0.1:54321 - "GET /api/1/tasks HTTP/1.1" 200 OK
INFO:     127.0.0.1:54322 - "POST /api/1/tasks HTTP/1.1" 201 Created
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  ...
```

**What to Look For:**
- Request method and path
- HTTP status codes (200, 201, 401, 404, 500)
- Exception tracebacks
- Database query logs (if echo=True)

**Frontend Logs (Terminal Running npm run dev):**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
- wait compiling /dashboard (client and server)...
- event compiled successfully in 150 ms
```

**What to Look For:**
- Compilation errors
- Build warnings
- Module resolution errors
- TypeScript type errors

---

### 2. Root Cause Identification

#### Purpose
Determine the underlying reason for the error, not just the symptom, to implement effective solutions.

#### The 5 Whys Technique

**Example Problem:** API returns 500 Internal Server Error

**Why 1:** Why is API returning 500?
- **Answer:** Exception thrown in backend route handler

**Why 2:** Why is exception thrown?
- **Answer:** Database query failed

**Why 3:** Why did database query fail?
- **Answer:** Foreign key constraint violation

**Why 4:** Why is there a foreign key violation?
- **Answer:** user_id doesn't exist in users table

**Why 5:** Why doesn't user_id exist?
- **Answer:** Better Auth hasn't created the user record yet

**Root Cause:** User record not created before task creation  
**Solution:** Ensure Better Auth properly creates user on signup

#### Root Cause Categories

**Category 1: Configuration Issues**

**Symptoms:**
- Environment variables not loaded
- Connections fail immediately
- "Not found" or "Missing" errors

**Root Causes:**
- Missing .env file
- Wrong environment variable names
- Typos in configuration values
- Not loading .env (missing load_dotenv())

**Example:**
```python
# Symptom: DATABASE_URL is None
# Root Cause: .env file not loaded

# Fix:
from dotenv import load_dotenv
load_dotenv()  # Add this line!
```

**Category 2: Dependency Issues**

**Symptoms:**
- ModuleNotFoundError
- ImportError
- Version conflicts
- "Cannot find module"

**Root Causes:**
- Package not installed
- Wrong package name
- Version incompatibility
- Not in virtual environment

**Example:**
```bash
# Symptom: ModuleNotFoundError: No module named 'fastapi'
# Root Cause: Package not installed in current environment

# Fix:
pip install fastapi
```

**Category 3: Logic Errors**

**Symptoms:**
- Wrong data returned
- Unexpected behavior
- Off-by-one errors
- NoneType errors

**Root Causes:**
- Incorrect conditional logic
- Wrong variable used
- Missing null checks
- Incorrect algorithm

**Example:**
```python
# Symptom: TypeError: 'NoneType' object is not subscriptable
# Root Cause: Not checking if result exists before accessing

# Bad:
user = session.get(User, user_id)
email = user.email  # Error if user is None!

# Fix:
user = session.get(User, user_id)
if user:
    email = user.email
else:
    raise HTTPException(404, "User not found")
```

**Category 4: Type Mismatches**

**Symptoms:**
- Type errors
- Cannot convert type X to Y
- Pydantic validation errors
- Database constraint errors

**Root Causes:**
- Wrong data type used
- Frontend sends string, backend expects int
- Database column type doesn't match model
- Missing type conversion

**Example:**
```python
# Symptom: Foreign key constraint error
# Root Cause: user_id type mismatch

# models.py - WRONG:
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)  # INTEGER type

class Task(SQLModel, table=True):
    user_id: str = Field(foreign_key="users.id")  # STRING type - MISMATCH!

# Fix: Make types match
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)  # STRING type

class Task(SQLModel, table=True):
    user_id: str = Field(foreign_key="users.id")  # STRING type - MATCH!
```

**Category 5: Timing/Order Issues**

**Symptoms:**
- Race conditions
- "Not initialized" errors
- Intermittent failures
- Works sometimes, fails other times

**Root Causes:**
- Code executed before dependencies ready
- Database connection not established
- Models imported before configuration
- Async operations not awaited

**Example:**
```python
# Symptom: Tables don't exist even though init_db() called
# Root Cause: Models not imported before init_db()

# main.py - WRONG ORDER:
from database import init_db
init_db()  # Called BEFORE models imported!
from models import Task  # Too late!

# Fix: Import models FIRST
from models import Task  # Import models FIRST
from database import init_db
init_db()  # Now Task model is known
```

**Category 6: Permission/Access Issues**

**Symptoms:**
- 403 Forbidden
- 401 Unauthorized
- "Access denied"
- Connection refused

**Root Causes:**
- Missing authentication token
- Wrong credentials
- Insufficient permissions
- Network/firewall blocking

**Example:**
```python
# Symptom: 403 Forbidden when accessing task
# Root Cause: User trying to access another user's task

# Fix: Check user_id matches
if task.user_id != current_user["user_id"]:
    raise HTTPException(403, "Cannot access other user's tasks")
```

#### Root Cause Diagnosis Tools

**Tool 1: Print Debugging**
```python
# Add print statements to trace execution
def get_task(task_id: int, user_id: str):
    print(f"DEBUG: Looking for task {task_id} for user {user_id}")
    task = session.get(Task, task_id)
    print(f"DEBUG: Found task: {task}")
    
    if task:
        print(f"DEBUG: Task owner: {task.user_id}")
        print(f"DEBUG: Current user: {user_id}")
        print(f"DEBUG: Match: {task.user_id == user_id}")
    
    return task
```

**Tool 2: Logging**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def verify_token(token: str):
    logger.debug(f"Token received: {token[:20]}...")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        logger.debug(f"Payload decoded: {payload}")
        return payload
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise
```

**Tool 3: Debugger (pdb)**
```python
import pdb

def problematic_function():
    pdb.set_trace()  # Execution pauses here
    # Step through code line by line
    result = complex_operation()
    return result
```

**Tool 4: Type Checking (mypy)**
```bash
# Install mypy
pip install mypy

# Run type checker
mypy backend/

# Finds type errors before runtime
```

**Tool 5: Database Query Logging**
```python
# Enable SQL echo
engine = create_engine(DATABASE_URL, echo=True)

# Now all SQL queries printed to console:
# SELECT tasks.id, tasks.title ... FROM tasks WHERE tasks.user_id = ?
```

---

### 3. Systematic Troubleshooting

#### Purpose
Follow a structured approach to isolate and fix errors efficiently without trial-and-error.

#### The Scientific Method for Debugging

**Step 1: Observe**
- What is the error message?
- When does it occur?
- What were you trying to do?
- Does it happen consistently?

**Step 2: Form Hypothesis**
- What do you think is causing it?
- Based on error message and stack trace
- Consider similar errors you've seen

**Step 3: Test Hypothesis**
- Create minimal reproducible example
- Test specific component in isolation
- Add logging/debugging output

**Step 4: Analyze Results**
- Did test confirm hypothesis?
- If yes, implement solution
- If no, form new hypothesis

**Step 5: Implement Solution**
- Make targeted fix
- Don't change multiple things at once
- Keep track of what you changed

**Step 6: Verify Fix**
- Test the specific error case
- Test related functionality
- Ensure no new errors introduced

#### Binary Search Debugging

**Principle:** Eliminate half the possibilities with each test

**Example: API endpoint not working**

```
Full request chain:
Frontend → API Client → Network → CORS → Auth Middleware → Route Handler → Database → Response

Test 1: Does backend receive request?
- Add log at route handler entry
- If YES: Problem is in handler or database
- If NO: Problem is before handler (network, CORS, auth)

Test 2: Does auth middleware pass?
- Add log after auth verification
- If YES: Problem is in route handler or database
- If NO: Problem is in authentication

Test 3: Does database query work?
- Add log before and after database call
- If YES: Problem is in response formatting
- If NO: Problem is in database query or connection

Continue until you isolate the exact point of failure
```

#### Isolation Testing

**Technique 1: Comment Out Code**
```python
def complex_function():
    part1()
    # part2()  # Comment out to test if part1 works alone
    # part3()
    part4()
```

**Technique 2: Minimal Reproduction**
```python
# Instead of full application, test component in isolation:

# test_database.py
from sqlmodel import create_engine
from models import Task

engine = create_engine(DATABASE_URL)

# Test just database connection
with engine.connect() as conn:
    print("Connection successful!")
```

**Technique 3: Stub External Dependencies**
```python
# Replace real API call with mock for testing:

# Original:
tasks = await api.getTasks()

# Stubbed for testing:
tasks = [
    {"id": 1, "title": "Test", "completed": False},
    {"id": 2, "title": "Test 2", "completed": True}
]
```

#### Checklist-Based Troubleshooting

**Backend Won't Start Checklist:**
- [ ] Virtual environment activated?
- [ ] Dependencies installed?
- [ ] .env file exists?
- [ ] DATABASE_URL set in .env?
- [ ] BETTER_AUTH_SECRET set in .env?
- [ ] load_dotenv() called?
- [ ] All imports successful?
- [ ] No syntax errors?
- [ ] Correct Python version (3.9+)?
- [ ] Port 8000 not already in use?

**API Returns 500 Error Checklist:**
- [ ] Check backend terminal for exception
- [ ] Read stack trace for error location
- [ ] Is database connected?
- [ ] Are tables created?
- [ ] Does user exist in database?
- [ ] Is foreign key valid?
- [ ] Are all required fields provided?
- [ ] Is data type correct?
- [ ] Is SQL query valid?
- [ ] Are relationships configured correctly?

**Frontend Can't Call Backend Checklist:**
- [ ] Backend server running?
- [ ] Correct API URL (http://localhost:8000)?
- [ ] CORS middleware added to backend?
- [ ] Correct origin in CORS config?
- [ ] JWT token included in request?
- [ ] Token format correct (Bearer {token})?
- [ ] Network tab shows request sent?
- [ ] Browser console shows error?
- [ ] Response status code?
- [ ] Response body content?

#### Progressive Complexity Testing

**Start Simple, Add Complexity:**

**Test 1: Basic Connection**
```bash
curl http://localhost:8000/
```
Expected: Response from backend

**Test 2: Unauthenticated Endpoint**
```bash
curl http://localhost:8000/docs
```
Expected: Swagger documentation

**Test 3: Create Mock Authenticated Endpoint**
```python
@app.get("/test")
def test():
    return {"message": "Working!"}
```
```bash
curl http://localhost:8000/test
```
Expected: {"message": "Working!"}

**Test 4: Add Authentication**
```python
@app.get("/test")
def test(user: dict = Depends(verify_token)):
    return {"message": f"Authenticated as {user['email']}"}
```
```bash
curl http://localhost:8000/test \
  -H "Authorization: Bearer {token}"
```
Expected: {"message": "Authenticated as ..."}

**Test 5: Add Database Query**
```python
@app.get("/test")
def test(
    user: dict = Depends(verify_token),
    session: Session = Depends(get_session)
):
    tasks = session.exec(select(Task)).all()
    return {"count": len(tasks)}
```

**By testing progressively, you isolate WHERE the problem is introduced**

---

### 4. Solution Implementation

#### Purpose
Implement fixes correctly without introducing new errors or breaking existing functionality.

#### Solution Implementation Principles

**Principle 1: One Change at a Time**
```python
# DON'T: Make multiple changes simultaneously
# Change 1: Fix import
# Change 2: Update function signature  
# Change 3: Modify database query
# Change 4: Update error handling

# If it breaks, you don't know which change caused it!

# DO: Make one change, test, then next change
# Change 1: Fix import → Test → Verify works
# Change 2: Update function signature → Test → Verify works
# Change 3: Modify database query → Test → Verify works
```

**Principle 2: Keep Working Code**
```python
# Before making changes, comment out working version:

# def get_tasks(user_id: int):  # OLD VERSION - WORKS
#     return session.query(Task).filter(Task.user_id == user_id).all()

# NEW VERSION - TESTING
def get_tasks(user_id: int):
    return session.exec(select(Task).where(Task.user_id == user_id)).all()

# If new version breaks, you can quickly revert
```

**Principle 3: Test Immediately**
```python
# After each fix, test immediately:

# 1. Make fix
def create_task(data: TaskCreate):
    task = Task(**data.dict())
    session.add(task)
    session.commit()
    return task

# 2. Test immediately
# curl -X POST http://localhost:8000/api/1/tasks -d '{"title":"Test"}'

# 3. Verify works before moving to next fix
```

**Principle 4: Understand Before Changing**
```python
# DON'T: Copy-paste solutions without understanding

# DO: Understand what each line does
from sqlmodel import Session, select

def get_task(session: Session, task_id: int):
    # Understand: select() creates SQL SELECT statement
    statement = select(Task).where(Task.id == task_id)
    
    # Understand: exec() executes the statement
    result = session.exec(statement)
    
    # Understand: first() returns first result or None
    task = result.first()
    
    return task
```

#### Solution Implementation Patterns

**Pattern 1: Environment Variable Fix**

**Problem:** DATABASE_URL is None

**Solution:**
```python
# 1. Create .env file (if missing)
# 2. Add DATABASE_URL
# 3. Load in code

# database.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment!")

engine = create_engine(DATABASE_URL)
```

**Verification:**
```bash
python -c "from database import DATABASE_URL; print('URL loaded:', DATABASE_URL[:30])"
```

**Pattern 2: Dependency Installation Fix**

**Problem:** ModuleNotFoundError

**Solution:**
```bash
# 1. Install missing package
pip install package_name

# 2. Add to requirements.txt
echo "package_name==version" >> requirements.txt

# 3. Verify installation
pip list | grep package_name

# 4. Test import
python -c "import package_name; print('✅ Imported successfully')"
```

**Pattern 3: CORS Configuration Fix**

**Problem:** CORS error in browser

**Solution:**
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware (MUST be before route includes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,  # Allow cookies/auth
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# THEN include routers
app.include_router(tasks.router)
```

**Verification:**
```bash
# Open browser console
# Make request from frontend
# Should see no CORS error
```

**Pattern 4: Database Connection Fix**

**Problem:** Cannot connect to database

**Solution:**
```python
# 1. Verify DATABASE_URL format
# Correct: postgresql://user:pass@host/db?sslmode=require
# Wrong: postgres://... (missing 'ql')
# Wrong: missing ?sslmode=require

# 2. Add connection parameters
from sqlmodel import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries
    pool_pre_ping=True,  # Verify connections before use
    pool_size=10,  # Connection pool size
    max_overflow=20  # Max additional connections
)

# 3. Test connection
with engine.connect() as conn:
    print("✅ Connected successfully!")
```

**Verification:**
```bash
python -c "from database import engine; engine.connect(); print('✅ Connection works')"
```

**Pattern 5: JWT Token Fix**

**Problem:** Token verification fails

**Solution:**
```python
# 1. Verify secrets match
# Check frontend .env.local:
cat frontend/.env.local | grep BETTER_AUTH_SECRET

# Check backend .env:
cat backend/.env | grep BETTER_AUTH_SECRET

# Must be IDENTICAL!

# 2. Verify token format in request
# Must be: Authorization: Bearer {token}
# NOT: Authorization: {token}
# NOT: Bearer {token} (missing header name)

# 3. Verify algorithm matches
# Backend:
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
                                              # Must match ↓
# Frontend Better Auth config:
jwt: {
  algorithm: "HS256"  # Must match
}

# 4. Add debugging
print(f"Token: {token[:20]}...")
print(f"Secret: {SECRET[:10]}...")
try:
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    print(f"✅ Decoded: {payload}")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Verification:**
```bash
# Test token creation and verification
python -c "
import jwt
SECRET = 'your-secret'
token = jwt.encode({'user_id': '123'}, SECRET, algorithm='HS256')
print('Token:', token)
decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
print('Decoded:', decoded)
"
```

#### Code Review Before Committing

**Before considering a fix complete:**

**Checklist:**
- [ ] Error no longer occurs
- [ ] Related functionality still works
- [ ] No new errors introduced
- [ ] Code is clean and readable
- [ ] Comments added if complex
- [ ] Debugging print statements removed (or converted to logging)
- [ ] No hardcoded values (use environment variables)
- [ ] No sensitive data exposed
- [ ] Type hints added (Python) or types correct (TypeScript)
- [ ] Imports organized and necessary

**Code Quality:**
```python
# BEFORE (messy debug code):
def get_task(id):
    print("getting task", id)  # Debug print
    t = session.query(Task).filter(Task.id == id).first()
    print("got task:", t)  # Debug print
    if t == None:  # Poor style
        return None
    else:
        return t

# AFTER (clean production code):
def get_task(task_id: int, session: Session) -> Optional[Task]:
    """
    Retrieve a task by ID.
    
    Args:
        task_id: The task ID to retrieve
        session: Database session
        
    Returns:
        Task if found, None otherwise
    """
    statement = select(Task).where(Task.id == task_id)
    task = session.exec(statement).first()
    return task
```

---

### 5. Verification & Testing

#### Purpose
Confirm that fixes work correctly and haven't introduced new issues.

#### Verification Levels

**Level 1: Unit Testing (Test Single Component)**

**Example: Test database connection**
```python
# test_database_connection.py
from database import engine

def test_connection():
    """Test that database connection works"""
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

**Level 2: Integration Testing (Test Components Together)**

**Example: Test API endpoint**
```bash
# Test complete request flow: Frontend → Backend → Database

# 1. Start backend
cd backend
uvicorn main:app --reload

# 2. Test endpoint
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing"}'

# Expected: 201 Created with task object
```

**Level 3: End-to-End Testing (Test Complete User Flow)**

**Example: Test complete signup → login → create task flow**
```
1. Open http://localhost:3000/signup
2. Fill form: email, password, name
3. Click Sign Up
4. Verify redirect to /dashboard
5. Fill task form: title, description
6. Click Create Task
7. Verify task appears in list
8. Click checkbox to complete task
9. Verify task marked complete
10. Click delete
11. Verify task removed
```

#### Testing Checklist

**After Fixing Backend Error:**
- [ ] Backend starts without errors
- [ ] No exceptions in terminal
- [ ] Database connection works
- [ ] Tables exist
- [ ] Can create record via API
- [ ] Can read record via API
- [ ] Can update record via API
- [ ] Can delete record via API
- [ ] Authentication works
- [ ] User isolation enforced

**After Fixing Frontend Error:**
- [ ] Frontend builds successfully
- [ ] No console errors
- [ ] Pages render correctly
- [ ] Forms submit successfully
- [ ] API calls work
- [ ] Loading states show
- [ ] Error states show
- [ ] Styling correct
- [ ] Responsive on mobile
- [ ] Navigation works

**After Fixing Integration Error:**
- [ ] Frontend can call backend
- [ ] CORS no longer blocks
- [ ] JWT tokens verifie