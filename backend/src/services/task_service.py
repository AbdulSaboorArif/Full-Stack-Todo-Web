from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


class TaskService:
    """Task service for business logic operations"""

    @staticmethod
    def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Get task by ID with user isolation"""
        return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    @staticmethod
    def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks for user"""
        return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
        """Create new task"""
        db_task = Task(**task.dict(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(db: Session, task_id: int, task: TaskUpdate, user_id: int) -> Optional[Task]:
        """Update existing task"""
        db_task = TaskService.get_task(db, task_id, user_id)
        if db_task is None:
            return None
        update_data = task.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> bool:
        """Delete task"""
        db_task = TaskService.get_task(db, task_id, user_id)
        if db_task is None:
            return False
        db.delete(db_task)
        db.commit()
        return True

    @staticmethod
    def complete_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Mark task as complete"""
        return TaskService.update_task(
            db,
            task_id,
            TaskUpdate(is_completed=True, completed_at=datetime.utcnow()),
            user_id
        )

    @staticmethod
    def incomplete_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Mark task as incomplete"""
        return TaskService.update_task(
            db,
            task_id,
            TaskUpdate(is_completed=False, completed_at=None),
            user_id
        )

    @staticmethod
    def validate_task_data(task: TaskCreate) -> None:
        """Validate task data"""
        if not task.title:
            raise ValueError("Task title is required")
        if len(task.title) > 255:
            raise ValueError("Task title cannot exceed 255 characters")
        if task.description and len(task.description) > 10000:
            raise ValueError("Task description cannot exceed 10,000 characters")