from better_auth import BetterAuth, BetterAuthSettings
from better_auth.jwt import JWTSettings
from .config.settings import Config
from .models.user import User
from .models.task import Task
from sqlmodel import Session, SQLModel
from datetime import timedelta


class AuthConfig:
    """Better Auth configuration for the Todo application"""

    @staticmethod
    def get_better_auth() -> BetterAuth:
        """Initialize Better Auth instance"""

        # JWT settings
        jwt_settings = JWTSettings(
            secret=Config.get_jwt_secret(),
            expiration=timedelta(days=7),  # 7 days expiration
            token_audience="todo-api",
            token_issuer="todo-app",
        )

        # Better Auth settings
        better_auth_settings = BetterAuthSettings(
            token_secret=Config.get_jwt_secret(),
            token_algorithm="HS256",
            token_expires_in=60 * 60 * 24 * 7,  # 7 days in seconds
            token_audience="todo-api",
            token_issuer="todo-app",
            user_entity=User,
            jwt_settings=jwt_settings,
        )

        # Initialize Better Auth
        better_auth = BetterAuth(settings=better_auth_settings)

        return better_auth