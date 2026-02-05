# Backend - Todo API

FastAPI backend for the Todo Full-Stack Web Application.

## Features

- JWT-based authentication using Better Auth
- User management with secure password hashing
- Task management with user isolation
- RESTful API endpoints
- Database integration with Neon Serverless PostgreSQL

## Requirements

- Python 3.11+
- UV package manager
- PostgreSQL database (Neon Serverless)

## Installation

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the development server:
   ```bash
   uv run uvicorn src.main:app --reload
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL="postgresql://user:password@localhost/todo_db"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-change-this-in-production"
BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
LOG_LEVEL="INFO"
ENVIRONMENT="development"
```

## API Documentation

Access the interactive API documentation at:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Development

### Running Tests
```bash
uv run pytest
```

### Code Quality
```bash
# Linting
uv run pylint src/
uv run flake8 src/

# Formatting
uv run black src/
uv run isort src/

# Type checking
uv run mypy src/
```

## Database

The application uses Neon Serverless PostgreSQL. Database migrations can be managed with Alembic.

## Project Structure

```
backend/
├── src/
│   ├── config/          # Configuration files
│   ├── models/          # SQLModel entities
│   ├── api/             # API routes
│   ├── services/        # Business logic
│   ├── middleware/      # Middleware components
│   └── main.py          # FastAPI application entry point
├── tests/              # Test suite
├── pyproject.toml      # Project configuration
└── .env.example       # Environment variables template
```

## License

This project is part of the Hackathon II Phase II Todo Full-Stack Web Application.