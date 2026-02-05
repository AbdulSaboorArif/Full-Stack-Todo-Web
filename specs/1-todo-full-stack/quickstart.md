---
# Quickstart Guide: Todo Full-Stack Web Application

**Branch**: `1-todo-full-stack` | **Date**: 2026-02-03 | **Spec**: `specs/1-todo-full-stack/spec.md`
**Input**: Feature specification from `/specs/1-todo-full-stack/spec.md`

## Development Environment Setup

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- UV package manager (recommended)
- Git
- A code editor (VS Code recommended)

### Project Structure
```
Full-Stack-Todo-Web/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── specs/            # Specifications and plans
└── .specify/         # Spec-Kit Plus configuration
```

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Dependencies
```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file with:
```env
# Database
DATABASE_URL="postgresql://user:password@localhost/todo_db"

# Authentication
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"

# CORS
BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

### 4. Database Setup
```bash
# Create database (adjust based on your setup)
createdb todo_db

# Run migrations (if using migrations)
uv run alembic upgrade head

# Or create tables directly
uv run python -c "from backend.main import engine; from backend.models import User, Task; User.metadata.create_all(engine); Task.metadata.create_all(engine)"
```

### 5. Start Backend Server
```bash
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# Or using yarn
yarn install
```

### 3. Environment Configuration
Create `.env.local` file with:
```env
# API URL
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Authentication
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"

# Development
NEXT_PUBLIC_ENVIRONMENT="development"
```

### 4. Start Frontend Development Server
```bash
npm run dev
# Or using yarn
yarn dev
```

## Running the Application

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### First Time Setup
1. Open http://localhost:3000
2. Click "Sign Up" to create a new account
3. Verify you can log in
4. Create your first task
5. Test task management features

## Development Workflow

### Backend Development
```bash
# Run backend with auto-reload
cd backend
uv run uvicorn backend.main:app --reload

# Run tests
cd backend
tox -e py
# Or
uv run pytest
```

### Frontend Development
```bash
# Run frontend with hot reload
cd frontend
npm run dev

# Run tests
cd frontend
npm run test
# Or
yarn test
```

### Database Operations
```bash
# Backend directory
cd backend

# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## Environment Variables Reference

### Backend Environment Variables
```env
DATABASE_URL="postgresql://..."          # Database connection string
BETTER_AUTH_SECRET="..."                 # JWT secret key
BACKEND_CORS_ORIGINS="http://localhost:3000"  # Allowed CORS origins
LOG_LEVEL="INFO"                         # Logging level
```

### Frontend Environment Variables
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"  # Backend API URL
NEXT_PUBLIC_ENVIRONMENT="development"      # Environment name
```

## Testing the Application

### Manual Testing
1. Register a new user
2. Log in with the new account
3. Create a task
4. View the task list
5. Update the task
6. Mark the task as complete
7. Delete the task
8. Log out and log back in to verify persistence

### API Testing
1. Access http://localhost:8000/docs for interactive API documentation
2. Test authentication endpoints
3. Test task management endpoints
4. Verify user isolation by testing with different users

## Troubleshooting

### Common Issues

**Issue**: Frontend cannot connect to backend
**Solution**: Check `NEXT_PUBLIC_API_URL` and backend server status

**Issue**: Authentication fails
**Solution**: Verify `BETTER_AUTH_SECRET` matches in both frontend and backend

**Issue**: Database connection fails
**Solution**: Check `DATABASE_URL` and database server status

**Issue**: CORS errors
**Solution**: Ensure `BACKEND_CORS_ORIGINS` includes frontend URL

### Debug Mode
```bash
# Backend with debug logging
uv run uvicorn backend.main:app --reload --log-level debug

# Frontend with debug mode
npm run dev
```

## Production Considerations

### Environment Setup
- Use different secrets for production
- Configure proper database credentials
- Set up HTTPS
- Configure proper logging and monitoring

### Deployment
- Frontend: Deploy to Vercel/Netlify
- Backend: Deploy to cloud service (AWS, GCP, etc.)
- Database: Use Neon Serverless PostgreSQL

---

*Quickstart guide complete. Development environment ready for implementation.*