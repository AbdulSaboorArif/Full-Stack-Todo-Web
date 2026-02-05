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


def get_current_user(token: str = None) -> User:
    """Get current user from JWT token"""
    from .main import engine
    from .config.settings import Config

    if not token:
        raise ValueError("Token is required")

    # Initialize Better Auth
    better_auth = AuthConfig.get_better_auth()

    # Verify token
    payload = better_auth.jwt.verify(token)

    # Get user from database
    with Session(engine) as session:
        user = session.get(User, payload["sub"])
        if not user:
            raise ValueError("User not found")
        return user


def get_current_user_id(token: str = None) -> int:
    """Get current user ID from JWT token"""
    user = get_current_user(token)
    return user.id