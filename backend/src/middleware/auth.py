from fastapi import Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .auth.config import JWTConfig
from .config.settings import Config
from fastapi import HTTPException, status
from typing import Callable, Awaitable
import jwt
from datetime import timedelta


class JWTAuthenticationMiddleware:
    """JWT authentication middleware for FastAPI"""

    def __init__(self, app: Callable) -> None:
        self.app = app

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Middleware call method"""

        # Skip authentication for open endpoints
        open_endpoints = [
            "/",
            "/health",
            "/docs",
            "/openapi.json",
            "/auth/login",
            "/auth/register",
        ]

        path = str(request.url)
        if any(path.startswith(endpoint) for endpoint in open_endpoints):
            return await call_next(request)

        # Get token from Authorization header
        authorization = request.headers.get("authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
            )

        token = authorization[len("Bearer ") :].strip()

        try:
            # Verify JWT token
            secret = JWTConfig.get_jwt_secret()
            algorithm = JWTConfig.get_jwt_algorithm()

            payload = jwt.decode(
                token,
                secret,
                algorithms=[algorithm]
            )

            from .models.user import User
            from .main import engine

            # Get user from database
            with Session(engine) as session:
                user = session.get(User, payload["sub"])
                if not user:
                    raise ValueError("User not found")
                request.state.user = user
                request.state.user_id = user.id
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {str(e)}",
            )

        # Call the next middleware/endpoint
        response = await call_next(request)
        return response