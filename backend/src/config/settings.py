import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# JWT configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

# CORS configuration
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

class Config:
    """Application configuration class"""

    @staticmethod
    def get_database_url() -> str:
        """Get database connection URL"""
        return DATABASE_URL

    @staticmethod
    def get_jwt_secret() -> str:
        """Get JWT secret key"""
        return BETTER_AUTH_SECRET

    @staticmethod
    def get_cors_origins() -> list[str]:
        """Get allowed CORS origins"""
        return [origin.strip() for origin in BACKEND_CORS_ORIGINS.split(",")]

    @staticmethod
    def get_log_level() -> str:
        """Get logging level"""
        return LOG_LEVEL

    @staticmethod
    def is_development() -> bool:
        """Check if environment is development"""
        return ENVIRONMENT.lower() == "development"