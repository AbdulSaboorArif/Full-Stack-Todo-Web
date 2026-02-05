# Auth Skill - Complete Definition

**Auth Skill** is a specialized capability focused on implementing secure user authentication mechanisms for the Phase II Todo Full-Stack Web Application. When invoked, this skill provides expertise in all aspects of user authentication using Better Auth with JWT tokens, connecting Next.js 16 frontend with FastAPI backend.

---

## Table of Contents

1. [Skill Purpose](#skill-purpose)
2. [Project-Specific Context](#project-specific-context)
3. [Core Components](#core-components)
   - [Signup Flows](#1-signup-flows)
   - [Signin Flows](#2-signin-flows)
   - [Password Hashing](#3-password-hashing)
   - [JWT Token Management](#4-jwt-token-management)
   - [Better Auth Integration](#5-better-auth-integration)
   - [Frontend-Backend Authentication Flow](#6-frontend-backend-authentication-flow)
4. [When to Invoke Auth Skill](#when-to-invoke-auth-skill)
5. [How Auth Skill Works](#how-auth-skill-works)
6. [Auth Skill Output](#auth-skill-output)
7. [Implementation Patterns](#implementation-patterns)
8. [Security Checklist](#security-checklist)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## Skill Purpose

Auth Skill enables you to design, implement, and troubleshoot the complete authentication system for the hackathon todo application. It covers:

- User registration (signup) with email/password
- User login (signin) with credential verification
- Secure password storage using bcrypt hashing
- Token-based authentication using JWT
- Better Auth framework integration
- Frontend-backend authentication coordination
- User session management
- Protected route implementation
- User isolation and access control

This skill ensures secure, production-ready authentication that follows industry best practices and meets the Phase II project requirements.

---

## Project-Specific Context

This skill operates within the Phase II requirements:

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 16 + Better Auth | User interface and auth client |
| Backend | FastAPI + PyJWT | API server and token verification |
| Authentication | JWT tokens | Stateless authentication |
| Password Security | bcrypt | Secure password hashing |
| Token Storage | HTTP-only cookies | XSS-safe storage |
| Token Transmission | Authorization header | Bearer token pattern |

### Authentication Architecture

**The authentication system connects three main components:**

1. **Frontend (Next.js + Better Auth)**
   - Provides signup/signin UI
   - Issues JWT tokens on successful authentication
   - Stores tokens in HTTP-only cookies
   - Includes tokens in API requests

2. **Backend (FastAPI)**
   - Receives authentication requests
   - Verifies credentials against database
   - Hashes passwords with bcrypt
   - Generates and signs JWT tokens
   - Verifies JWT tokens on protected endpoints
   - Extracts user_id from tokens for data filtering

3. **Shared Secret (BETTER_AUTH_SECRET)**
   - Used by both frontend and backend
   - Signs JWT tokens (frontend/Better Auth)
   - Verifies JWT tokens (backend/FastAPI)
   - Must be 32+ cryptographically random characters
   - Stored in environment variables on both sides

### Authentication Requirements

**User Signup:**
- Email (required, unique, valid format)
- Password (required, min 8 chars, complexity rules)
- Name (required)
- Email verification (optional for Phase II)

**User Signin:**
- Email (required)
- Password (required)
- Returns JWT token on success
- Generic error message on failure

**Protected API Access:**
- All task endpoints require valid JWT token
- Token sent in Authorization: Bearer {token} header
- Backend verifies token on every request
- Backend extracts user_id from token
- Backend ensures URL user_id matches token user_id
- Invalid token → 401 Unauthorized
- Valid token but wrong user → 403 Forbidden

**Security Rules:**
- Passwords hashed with bcrypt (never plaintext)
- JWT tokens expire after 7 days
- Same BETTER_AUTH_SECRET on frontend and backend
- HTTPS enforced in production
- HTTP-only cookies prevent XSS
- Rate limiting on auth endpoints (5 attempts per 15 min)

---

## Core Components

### 1. Signup Flows

#### Purpose
Enable new users to create accounts with email and password, ensuring data validation, password security, and proper user record creation.

#### Frontend Signup (Next.js + Better Auth)

**User Journey:**
1. User navigates to /signup page
2. User fills form with email, password, name
3. Frontend validates email format and password strength
4. User clicks "Sign Up" button
5. Better Auth signUp() method called
6. Request sent to Better Auth API route
7. Better Auth forwards to backend /auth/signup
8. Backend creates user and returns success
9. Frontend redirects to /login or auto-signs in to /dashboard
10. On error, display validation or server error messages

**Frontend Implementation Responsibilities:**
- Create signup page (app/signup/page.tsx)
- Build signup form with email, password, name inputs
- Implement client-side validation:
  - Email format: valid email pattern
  - Password strength: min 8 chars, uppercase, lowercase, number, special char
  - Name: not empty
- Display validation errors inline
- Call Better Auth signUp() on form submission
- Handle loading state during signup
- Handle errors and display user-friendly messages
- Redirect on successful signup

**Better Auth signUp() Method:**
```
Call signUp.email({
  email: user@example.com,
  password: SecurePass123!,
  name: John Doe
})

Better Auth:
1. Sends POST to /api/auth/signup (Next.js API route)
2. Next.js API route forwards to backend /auth/signup
3. Waits for response
4. On success: creates session (optional)
5. On error: throws exception with error message
```

#### Backend Signup (FastAPI)

**Endpoint:** POST /auth/signup

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Backend Processing Steps:**
1. Receive POST /auth/signup request
2. Validate email format using regex pattern
3. Check email length (max 254 characters)
4. Query database to check if email already exists
5. If exists: return 400 "Email already registered"
6. Validate password strength:
   - Minimum 8 characters
   - Contains uppercase letter
   - Contains lowercase letter
   - Contains number
   - Contains special character
7. If invalid: return 400 with validation errors
8. Hash password using bcrypt.hash() with cost factor 12
9. Create User model with hashed password
10. Insert user into database (transaction)
11. Return success response

**Response (Success):**
```json
{
  "success": true,
  "user_id": "123",
  "email": "user@example.com"
}
```

**Response (Error):**
```json
{
  "detail": "Email already registered"
}
// or
{
  "detail": "Password must contain uppercase letter"
}
```

#### Password Hashing on Signup

**Critical Rule: NEVER store plaintext passwords**

**Hashing Process:**
```
1. Receive plain password from frontend (over HTTPS)
2. Import bcrypt library
3. Call bcrypt.hash(password, cost_factor=12)
4. Bcrypt automatically:
   - Generates unique random salt
   - Combines salt with password
   - Hashes using bcrypt algorithm
   - Returns hash string (includes salt)
5. Store ONLY the hash in database
6. NEVER log or display the password
```

**Why bcrypt?**
- Industry standard for password hashing
- Automatically handles salt generation
- Configurable cost factor for security/speed balance
- Resistant to rainbow table attacks
- Constant-time verification (prevents timing attacks)

**Cost Factor:**
- Cost of 12 = ~250ms computation time
- Cost of 14 = ~1000ms computation time
- Higher cost = more secure but slower
- Recommended: 12 for good balance

**What gets stored:**
```
Original password: "SecurePass123!"
Stored in database: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5VC8N0ijGCOjG"

The stored hash includes:
- $2b$ = bcrypt algorithm identifier
- 12 = cost factor
- Next 22 chars = salt (automatically generated)
- Remaining chars = actual hash
```

#### Signup Security Principles

**Email Validation:**
- Check format matches: name@domain.extension
- Verify length under 254 characters
- Block disposable email domains (optional)
- Check uniqueness in database
- Normalize to lowercase before storage

**Password Validation:**
- Minimum length: 8 characters (12+ recommended)
- Require complexity:
  - At least one uppercase letter (A-Z)
  - At least one lowercase letter (a-z)
  - At least one number (0-9)
  - At least one special character (!@#$%^&*)
- Check against common passwords list
- Maximum length: 128 characters (prevent DoS)

**Error Messages:**
- Be specific for validation errors (help user fix issues)
- Be generic for duplicate email (avoid account enumeration)
- Never reveal if email exists in database
- Use same error format consistently

**Database Transaction:**
- Use atomic transaction for user creation
- Rollback on any error
- Ensure email uniqueness with database constraint
- Log signup events for monitoring

**Rate Limiting:**
- Maximum 3 signup attempts per hour per IP
- Prevents automated account creation
- Returns 429 Too Many Requests when exceeded

#### Signup Flow Diagram
```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Fill form (email, password, name)
     ▼
┌─────────────────┐
│ Next.js Signup  │
│      Form       │
└────┬────────────┘
     │
     │ 2. Validate inputs
     │    - Email format
     │    - Password strength
     ▼
┌─────────────────┐
│  Better Auth    │
│   signUp()      │
└────┬────────────┘
     │
     │ 3. POST /api/auth/signup
     ▼
┌─────────────────┐
│   Next.js API   │
│      Route      │
└────┬────────────┘
     │
     │ 4. Forward to backend
     ▼
┌─────────────────┐
│  FastAPI        │
│  /auth/signup   │
└────┬────────────┘
     │
     │ 5. Validate email uniqueness
     │ 6. Validate password strength
     ▼
┌─────────────────┐
│     bcrypt      │
│ Hash Password   │
└────┬────────────┘
     │
     │ 7. Store hash (not plaintext)
     ▼
┌─────────────────┐
│    Database     │
│  Insert User    │
└────┬────────────┘
     │
     │ 8. Return success
     ▼
┌─────────────────┐
│  Better Auth    │
│ Create Session  │
└────┬────────────┘
     │
     │ 9. Redirect to dashboard
     ▼
┌─────────────────┐
│    Dashboard    │
└─────────────────┘
```

---

### 2. Signin Flows

#### Purpose
Authenticate existing users by verifying their credentials, issuing JWT tokens, and establishing secure sessions.

#### Frontend Signin (Next.js + Better Auth)

**User Journey:**
1. User navigates to /login page
2. User fills form with email and password
3. User clicks "Sign In" button
4. Better Auth signIn() method called
5. Request sent to Better Auth API route
6. Better Auth forwards to backend /auth/signin
7. Backend verifies credentials and returns JWT token
8. Better Auth stores JWT token in HTTP-only cookie
9. Better Auth creates user session
10. Frontend redirects to /dashboard
11. On error, display "Invalid credentials" message

**Frontend Implementation Responsibilities:**
- Create login page (app/login/page.tsx)
- Build signin form with email and password inputs
- No need for complex validation (backend will verify)
- Call Better Auth signIn() on form submission
- Handle loading state during signin
- Handle errors with generic message: "Invalid email or password"
- Never reveal whether email or password was wrong
- Redirect to /dashboard on successful signin
- Store user session state

**Better Auth signIn() Method:**
```
Call signIn.email({
  email: user@example.com,
  password: SecurePass123!
})

Better Auth:
1. Sends POST to /api/auth/signin (Next.js API route)
2. Next.js API route forwards to backend /auth/signin
3. Backend verifies credentials and returns JWT token
4. Better Auth receives { token: "eyJhbG...", user: {...} }
5. Better Auth stores token in HTTP-only cookie
6. Better Auth creates session object
7. Returns success to frontend
8. On error: throws exception with "Invalid credentials"
```

#### Backend Signin (FastAPI)

**Endpoint:** POST /auth/signin

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Backend Processing Steps:**
1. Receive POST /auth/signin request
2. Extract email and password from request body
3. Query database: SELECT * FROM users WHERE email = ?
4. If user not found:
   - Don't reveal email doesn't exist
   - Return 401 "Invalid credentials"
5. If user found:
   - Retrieve hashed_password from user record
   - Call bcrypt.verify(submitted_password, stored_hash)
   - If verification fails:
     - Don't reveal password is wrong
     - Return 401 "Invalid credentials"
   - If verification succeeds:
     - Proceed to token generation
6. Generate JWT token:
   - Create payload with user_id, email, expiration
   - Sign with BETTER_AUTH_SECRET
   - Set expiration to 7 days from now
7. Return success response with token and user info

**Response (Success):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQwMDAwMDAwfQ.signature",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Response (Error):**
```json
{
  "detail": "Invalid credentials"
}
```

#### Password Verification

**Critical Rule: Use constant-time comparison**

**Verification Process:**
```
1. User submits plain password
2. Backend retrieves hashed_password from database
3. Call bcrypt.verify(plain_password, hashed_password)
4. bcrypt.verify() internally:
   - Extracts salt from stored hash
   - Hashes submitted password with same salt
   - Compares new hash with stored hash
   - Uses constant-time comparison (prevents timing attacks)
5. Returns True if match, False if no match
6. Based on result:
   - True: proceed with signin
   - False: return 401 "Invalid credentials"
```

**Why constant-time comparison?**
- Prevents timing attacks
- Attacker cannot determine correctness by measuring response time
- bcrypt handles this automatically

**Password Verification Code Pattern:**
```
Backend (Python with passlib):

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# When user signs in
user = db.query(User).filter(User.email == email).first()

if not user:
    # User doesn't exist
    raise HTTPException(401, "Invalid credentials")

is_valid = pwd_context.verify(plain_password, user.hashed_password)

if not is_valid:
    # Password is wrong
    raise HTTPException(401, "Invalid credentials")

# Password is correct, proceed to generate token
```

#### JWT Token Generation

**Token Structure:**

A JWT token consists of three parts separated by dots:
```
header.payload.signature

Example:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQwMDAwMDAwfQ.signature_here
```

**Part 1: Header (base64url encoded)**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
- alg: Algorithm used (HMAC SHA256)
- typ: Token type (JWT)

**Part 2: Payload (base64url encoded)**
```json
{
  "user_id": "123",
  "email": "user@example.com",
  "iat": 1735000000,
  "exp": 1740000000
}
```
- user_id or sub: User's unique identifier (REQUIRED)
- email: User's email address (optional but useful)
- iat: Issued at timestamp (Unix timestamp)
- exp: Expiration timestamp (Unix timestamp, 7 days from iat)
- iss: Issuer (optional, e.g., "todo-app")

**Part 3: Signature**
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  BETTER_AUTH_SECRET
)
```
- Ensures token hasn't been tampered with
- Only valid if signed with correct secret

**Token Generation Code Pattern:**
```
Backend (Python with PyJWT):

import jwt
from datetime import datetime, timedelta
import os

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

def generate_jwt_token(user_id: str, email: str) -> str:
    now = datetime.utcnow()
    
    payload = {
        "user_id": user_id,
        "email": email,
        "iat": now,
        "exp": now + timedelta(days=7)
    }
    
    token = jwt.encode(
        payload,
        BETTER_AUTH_SECRET,
        algorithm="HS256"
    )
    
    return token
```

**Token Payload Design Principles:**
- Keep payload small (sent with every request)
- Include only necessary claims
- Don't put sensitive data (payload is base64, not encrypted)
- Anyone can decode and read payload
- Signature proves it hasn't been modified
- Use short expiration for security

**Token Expiration Strategy:**
- Default: 7 days from issuance
- Balance: security vs. user convenience
- Shorter = more secure, more frequent re-logins
- Longer = less secure, fewer re-logins
- For Phase II: 7 days is appropriate
- Production: consider shorter (1-24 hours) with refresh tokens

#### Signin Security Principles

**Credential Verification:**
- Always check both email and password
- Use constant-time comparison for passwords
- Never reveal which credential is wrong
- Always return same error: "Invalid credentials"

**Generic Error Messages:**
- Don't say "Email not found" (reveals email exists)
- Don't say "Password incorrect" (reveals email is valid)
- Always say "Invalid credentials" for all failures
- Prevents account enumeration attacks

**Rate Limiting:**
- Maximum 5 signin attempts per 15 minutes per email
- Prevents brute force password attacks
- Returns 429 Too Many Requests when exceeded
- Track attempts by email address and IP

**Logging:**
- Log all signin attempts (success and failure)
- Include timestamp, email, IP address, user agent
- Don't log passwords (even hashed)
- Monitor for suspicious patterns
- Alert on multiple failures

**Session Management:**
- Better Auth creates session on successful signin
- Session stored in HTTP-only cookie
- Cookie sent automatically with requests
- Cookie has Secure flag (HTTPS only in production)
- Cookie has SameSite=Strict (CSRF protection)

#### Signin Flow Diagram
```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Enter email and password
     ▼
┌─────────────────┐
│ Next.js Login   │
│      Form       │
└────┬────────────┘
     │
     │ 2. Click Sign In
     ▼
┌─────────────────┐
│  Better Auth    │
│   signIn()      │
└────┬────────────┘
     │
     │ 3. POST /api/auth/signin
     ▼
┌─────────────────┐
│   Next.js API   │
│      Route      │
└────┬────────────┘
     │
     │ 4. Forward to backend
     ▼
┌─────────────────┐
│  FastAPI        │
│  /auth/signin   │
└────┬────────────┘
     │
     │ 5. Query user by email
     ▼
┌─────────────────┐
│    Database     │
│   Find User     │
└────┬────────────┘
     │
     │ 6. Return user with hashed_password
     ▼
┌─────────────────┐
│     bcrypt      │
│Verify Password  │
└────┬────────────┘
     │
     │ 7. Password correct?
     ├─ No  → Return 401 "Invalid credentials"
     │
     └─ Yes → Continue
     ▼
┌─────────────────┐
│   Generate JWT  │
│  Sign with      │
│ BETTER_AUTH_    │
│    SECRET       │
└────┬────────────┘
     │
     │ 8. Return { token, user }
     ▼
┌─────────────────┐
│  Better Auth    │
│ Store token in  │
│   HTTP-only     │
│     cookie      │
└────┬────────────┘
     │
     │ 9. Create session
     ▼
┌─────────────────┐
│  Redirect to    │
│   /dashboard    │
└─────────────────┘
```

---

### 3. Password Hashing

#### Purpose
Ensure passwords are stored securely and cannot be recovered even if the database is compromised.

#### Why Password Hashing is Critical

**The Problem with Plaintext Passwords:**
- If database is breached, all passwords exposed
- Users often reuse passwords across sites
- Attackers gain access to other accounts
- Company liable for negligence
- Reputation damage
- Legal consequences (GDPR, etc.)

**The Solution: Cryptographic Hashing:**
- Transform password into irreversible hash
- Store only the hash, never the password
- Even database admin cannot see passwords
- Breach exposes hashes, not passwords
- Passwords remain secure

#### bcrypt Algorithm

**What is bcrypt?**
- Industry-standard password hashing function
- Specifically designed for password security
- Based on Blowfish cipher
- Introduced in 1999, still secure today
- Used by major platforms (Facebook, Twitter, etc.)

**Why bcrypt?**
- Slow by design (prevents brute force)
- Automatically handles salt generation
- Salt stored with hash (no separate storage needed)
- Configurable cost factor (adaptive to hardware improvements)
- Resistant to rainbow table attacks
- Constant-time verification (prevents timing attacks)

**Alternatives:**
- **argon2**: Newer, more secure, winner of Password Hashing Competition
- **scrypt**: Memory-hard, good but less common
- **PBKDF2**: Older, still acceptable but bcrypt preferred
- **DO NOT USE**: MD5, SHA1, SHA256 (too fast, designed for data integrity not passwords)

#### bcrypt Configuration

**Cost Factor (Work Factor):**
- Determines number of hashing iterations
- Formula: iterations = 2^cost
- Higher cost = more secure = slower

**Cost Factor Guidelines:**
| Cost | Iterations | Time | Use Case |
|------|-----------|------|----------|
| 10 | 1,024 | ~100ms | Minimum acceptable |
| 12 | 4,096 | ~250ms | **Recommended for Phase II** |
| 14 | 16,384 | ~1000ms | High security applications |
| 16 | 65,536 | ~4000ms | Maximum practical |

**Choosing Cost Factor:**
- Balance security vs. user experience
- Too low: vulnerable to brute force
- Too high: slow signup/signin
- Recommendation: Start with 12, adjust based on performance
- Increase cost factor over time as hardware improves

#### Salt Generation

**What is a Salt?**
- Random data added to password before hashing
- Ensures same password hashes to different values
- Prevents rainbow table attacks
- Stored alongside hash (not secret)

**How bcrypt Handles Salts:**
- Automatically generates unique random salt per password
- No manual salt management needed
- Salt included in hash output
- Salt extracted automatically during verification

**Salt Example:**
```
Password: "SecurePass123!"
Salt 1:   "randomly_generated_22_chars_1"
Salt 2:   "randomly_generated_22_chars_2"

Hash 1:   "$2b$12$randomly_generated_22_chars_1hash_output_here"
Hash 2:   "$2b$12$randomly_generated_22_chars_2different_hash_here"

Same password → Different hashes (due to different salts)
```

#### Password Hashing Implementation

**Backend (Python with passlib):**

**Step 1: Install passlib**
```bash
pip install passlib[bcrypt]
```

**Step 2: Create Password Context**
```python
from passlib.context import CryptContext

# Create context with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12  # Cost factor
)
```

**Step 3: Hash Password (on Signup)**
```python
def hash_password(plain_password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        plain_password: User's plain text password
    
    Returns:
        Hashed password string (includes salt and algorithm info)
    """
    hashed = pwd_context.hash(plain_password)
    return hashed

# Example usage
user_password = "SecurePass123!"
hashed_password = hash_password(user_password)
# Store hashed_password in database

# Result looks like:
# "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5VC8N0ijGCOjG"
```

**Step 4: Verify Password (on Signin)**
```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: User's submitted password
        hashed_password: Stored hash from database
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

# Example usage
submitted_password = "SecurePass123!"
stored_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5VC8N0ijGCOjG"

is_valid = verify_password(submitted_password, stored_hash)
if is_valid:
    # Password correct, proceed with signin
    generate_token()
else:
    # Password incorrect
    raise HTTPException(401, "Invalid credentials")
```

#### Hash Format Breakdown

**bcrypt Hash Structure:**
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5VC8N0ijGCOjG
 │  │  │                      │
 │  │  │                      └─ Actual hash (31 chars)
 │  │  └─ Salt (22 chars)
 │  └─ Cost factor (12)
 └─ Algorithm version ($2b$ = bcrypt)
```

**Components:**
1. **$2b$**: Algorithm identifier (bcrypt variant)
2. **12**: Cost factor (2^12 = 4096 iterations)
3. **Next 22 chars**: Random salt (base64 encoded)
4. **Remaining chars**: Actual password hash

**Important Notes:**
- Everything needed for verification is in the hash
- No separate salt storage required
- Hash format is standard across implementations
- Can migrate hashes between systems

#### Password Hashing Best Practices

**Storage Rules:**
- ✅ Store only the bcrypt hash in database
- ✅ Use VARCHAR(255) for hash column
- ❌ Never store plaintext password
- ❌ Never log passwords (plain or hashed)
- ❌ Never send passwords via email
- ❌ Never display passwords to users or admins

**Hashing Rules:**
- ✅ Hash on backend only (not frontend)
- ✅ Use bcrypt or argon2
- ✅ Use cost factor 12 or higher
- ✅ Let library handle salt generation
- ❌ Never use MD5, SHA1, or SHA256 for passwords
- ❌ Never implement your own hashing algorithm
- ❌ Never hash on frontend (security theater)

**Verification Rules:**
- ✅ Use constant-time comparison (bcrypt does this)
- ✅ Return generic error for wrong password
- ✅ Rate limit signin attempts
- ❌ Never reveal if email or password was wrong
- ❌ Never implement password hints
- ❌ Never allow password recovery (only reset)

**Database Schema:**
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,  -- Store hash here
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Note: Column is named 'hashed_password' not 'password'
-- Makes it clear this is hashed, not plaintext
```

#### Security Considerations

**Protection Against Attacks:**

**1. Rainbow Table Attacks:**
- Attacker pre-computes hashes of common passwords
- Salt makes rainbow tables useless
- Each password has unique salt
- Must recompute for each user

**2. Brute Force Attacks:**
- Attacker tries many passwords
- Slow hashing (cost 12) makes this impractical
- 250ms per attempt = 345,600 attempts per day
- Combined with rate limiting: very slow

**3. Timing Attacks:**
- Attacker measures response time
- bcrypt uses constant-time comparison
- Cannot determine correctness from timing

**4. Database Breach:**
- Attacker steals database
- Gets hashed passwords, not plaintext
- Must crack each hash individually
- With cost 12, very time-consuming

**Cost Factor and Security:**
```
Cost 10: 1 billion hashes/sec GPU = 1024 hashes/sec
Cost 12: 1 billion hashes/sec GPU = 256 hashes/sec
Cost 14: 1 billion hashes/sec GPU = 64 hashes/sec

To crack 8-char password with cost 12:
- Possible combinations: 96^8 = 7.2 quadrillion
- At 256 hashes/sec: 892 million years
```

**Migration Strategy:**
If upgrading from old hashing:

Don't force password reset
On next signin, verify with old method
If valid, rehash with bcrypt
Update database with new hash
Gradually migrate all users
Eventually deprecate old method
---
