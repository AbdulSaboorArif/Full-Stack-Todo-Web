from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from .user import User


class Task(SQLModel, table=True):
    """Task entity representing a user task"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="User.id", index=True)
    title: str
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationship to User
    user: Optional[User] = Relationship()

    def __repr__(self) -> str:
        status = "completed" if self.is_completed else "incomplete"
        return f"<Task id={self.id} user_id={self.user_id} title={self.title!r} status={status}>"


class TaskCreate(SQLModel):
    """Pydantic model for creating tasks"""

    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    """Pydantic model for updating tasks"""

    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None