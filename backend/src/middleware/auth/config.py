from datetime import timedelta
from .config.settings import Config
from .models.user import User
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from .database import get_db


class JWTConfig:
    """JWT configuration for the Todo application"""

    @staticmethod
    def get_jwt_secret() -> str:
        """Get JWT secret key"""
        return Config.get_jwt_secret()

    @staticmethod
    def get_jwt_algorithm() -> str:
        """Get JWT algorithm"""
        return "HS256"

    @staticmethod
    def get_jwt_expiration() -> int:
        """Get JWT expiration time in seconds"""
        return 7 * 24 * 60 * 60  # 7 days in seconds