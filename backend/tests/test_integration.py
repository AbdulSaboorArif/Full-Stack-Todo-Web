import pytest
import httpx
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from unittest.mock import patch

from backend.src.main import app
from backend.src.database import get_db, init_db
from backend.src.models.user import User
from backend.src.models.task import Task

# Test setup
client = TestClient(app)

# Test data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

# Fixtures
@pytest.fixture
def test_db():
    """Create test database"""
    init_db()
    yield
    # Clean up
    from backend.src.database import engine
    from sqlalchemy import text
    with Session(engine) as session:
        session.execute(text("DROP TABLE tasks;"))
        session.execute(text("DROP TABLE users;"))
        session.commit()

@pytest.fixture
def test_user(test_db):
    """Create test user"""
    response = client.post("/auth/register", json={
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    })
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def test_token(test_user):
    """Get test user token"""
    response = client.post("/auth/login", data={
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    })
    assert response.status_code == 200
    return response.json()["access_token"]

# Tests

def test_health_check(test_db):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(test_db):
    """Test user registration"""
    # Register new user
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "newpassword123"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == "newuser@example.com"

    # Try to register same email again
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "newpassword123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_user(test_db, test_user):
    """Test user login"""
    # Login with correct credentials
    response = client.post("/auth/login", data={
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # Login with wrong password
    response = client.post("/auth/login", data={
        "username": TEST_USER_EMAIL,
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect" in response.json()["detail"]

    # Login with non-existent user
    response = client.post("/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "password"
    })
    assert response.status_code == 401
    assert "Incorrect" in response.json()["detail"]


def test_task_crud(test_db, test_token):
    """Test task CRUD operations"""
    headers = {"Authorization": f"Bearer {test_token}"}

    # Create task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"
    assert task["description"] == "This is a test task"
    assert task["is_completed"] == False
    assert "id" in task

    task_id = task["id"]

    # Get all tasks
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"

    # Get specific task
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

    # Update task
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "is_completed": True
    }
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated description"
    assert updated_task["is_completed"] == True

    # Mark as incomplete
    response = client.patch(f"/tasks/{task_id}/incomplete", headers=headers)
    assert response.status_code == 200
    incomplete_task = response.json()
    assert incomplete_task["is_completed"] == False

    # Delete task
    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    # Verify task is deleted
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 404


def test_user_isolation(test_db, test_token):
    """Test user isolation"""
    headers = {"Authorization": f"Bearer {test_token}"}

    # Create first user's task
    task_data = {"title": "User 1 Task"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Register second user
    response = client.post("/auth/register", json={
        "email": "user2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200

    # Login second user
    response = client.post("/auth/login", data={
        "username": "user2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    second_token = response.json()["access_token"]
    second_headers = {"Authorization": f"Bearer {second_token}"}

    # Second user should not see first user's task
    response = client.get(f"/tasks/{task_id}", headers=second_headers)
    assert response.status_code == 404

    # Second user can create their own tasks
    task_data = {"title": "User 2 Task"}
    response = client.post("/tasks/", json=task_data, headers=second_headers)
    assert response.status_code == 200

    # First user should only see their own task
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "User 1 Task"


def test_invalid_token(test_db):
    """Test invalid token handling"""
    # Invalid token
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]

    # No token
    response = client.get("/tasks/")
    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]


def test_open_endpoints(test_db):
    """Test open endpoints (no authentication required)"""
    # Health check
    response = client.get("/health")
    assert response.status_code == 200

    # Root
    response = client.get("/")
    assert response.status_code == 200

    # Docs (if available)
    response = client.get("/docs")
    assert response.status_code == 200 or response.status_code == 404