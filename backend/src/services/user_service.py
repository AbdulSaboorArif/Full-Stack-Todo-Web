from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..models.user import User, UserCreate
from ..models.task import Task
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """User service for business logic operations"""

    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create new user"""
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, password_hash=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, email: Optional[str] = None) -> Optional[User]:
        """Update user email"""
        db_user = UserService.get_user(db, user_id)
        if db_user is None:
            return None
        if email:
            existing_user = UserService.get_user_by_email(db, email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
            db_user.email = email
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user"""
        db_user = UserService.get_user(db, user_id)
        if db_user is None:
            return False
        db.delete(db_user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks for user"""
        return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

# Helper functions

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


class UserValidator:
    """User data validation"""

    @staticmethod
    def validate_email(email: str) -> None:
        """Validate email format"""
        if not email:
            raise ValueError("Email is required")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email format")
        if len(email) > 255:
            raise ValueError("Email cannot exceed 255 characters")

    @staticmethod
    def validate_password(password: str) -> None:
        """Validate password strength"""
        if not password:
            raise ValueError("Password is required")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(password) > 128:
            raise ValueError("Password cannot exceed 128 characters")

    @staticmethod
    def validate_user_create(user: UserCreate) -> None:
        """Validate user creation data"""
        UserValidator.validate_email(user.email)
        UserValidator.validate_password(user.password)