from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from ..database import get_db
from ..models.user import User
from ..middleware.auth.config import JWTConfig
from ..config.settings import Config

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    email: str
    id: int

# Helper functions

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    secret = JWTConfig.get_jwt_secret()
    algorithm = JWTConfig.get_jwt_algorithm()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)

# Routes

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """Register new user"""
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = create_user(db, user)
    return UserOut(email=user.email, id=user.id)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    """Login user"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(days=7)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=UserOut)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
    """Get current user from token"""
    payload = jwt.decode(token, JWTConfig.get_jwt_secret(), algorithms=[JWTConfig.get_jwt_algorithm()])
    user = get_user(db, payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return UserOut(email=user.email, id=user.id)

@router.post("/logout")
async def logout() -> dict[str, str]:
    """Logout user"""
    return {"message": "Successfully logged out"}