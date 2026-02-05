from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from ..middleware.auth import get_current_user_id

router = APIRouter()

# Helper functions

def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Get task by ID with user isolation"""
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    """Get all tasks for user"""
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
    """Create new task"""
    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate, user_id: int) -> Optional[Task]:
    """Update existing task"""
    db_task = get_task(db, task_id, user_id)
    if db_task is None:
        return None
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """Delete task"""
    db_task = get_task(db, task_id, user_id)
    if db_task is None:
        return False
    db.delete(db_task)
    db.commit()
    return True

# Pydantic models
class TaskOut(Task):
    """Task output model"""
    class Config:
        from_attributes = True

class TaskCreateOut(TaskCreate):
    """Task create output model"""
    class Config:
        from_attributes = True

# Routes

@router.get("/", response_model=List[TaskOut])
async def read_tasks(skip: int = 0, limit: int = 100, current_user_id: int = Depends(get_current_user_id)) -> List[TaskOut]:
    """Get all tasks for current user"""
    db = next(get_db())
    tasks = get_tasks(db, current_user_id, skip, limit)
    return tasks

@router.post("/", response_model=TaskOut)
async def create_user_task(task: TaskCreate, current_user_id: int = Depends(get_current_user_id)) -> TaskOut:
    """Create new task for current user"""
    db = next(get_db())
    db_task = create_task(db, task, current_user_id)
    return db_task

@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: int, current_user_id: int = Depends(get_current_user_id)) -> TaskOut:
    """Get specific task for current user"""
    db = next(get_db())
    db_task = get_task(db, task_id, current_user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=TaskOut)
async def update_user_task(
    task_id: int,
    task: TaskUpdate,
    current_user_id: int = Depends(get_current_user_id)
) -> TaskOut:
    """Update existing task for current user"""
    db = next(get_db())
    db_task = update_task(db, task_id, task, current_user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
async def delete_user_task(
    task_id: int,
    current_user_id: int = Depends(get_current_user_id)
) -> dict[str, str]:
    """Delete task for current user"""
    db = next(get_db())
    success = delete_task(db, task_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_user_id: int = Depends(get_current_user_id)
) -> TaskOut:
    """Mark task as complete"""
    db = next(get_db())
    db_task = update_task(db, task_id, TaskUpdate(is_completed=True), current_user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/incomplete")
async def incomplete_task(
    task_id: int,
    current_user_id: int = Depends(get_current_user_id)
) -> TaskOut:
    """Mark task as incomplete"""
    db = next(get_db())
    db_task = update_task(db, task_id, TaskUpdate(is_completed=False), current_user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task