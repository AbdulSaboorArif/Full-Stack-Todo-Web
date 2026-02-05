from fastapi import APIRouter
from .auth import router as auth_router
from .tasks import router as tasks_router

# Main API router
api_router = APIRouter()

# Include auth routes
api_router.include_router(auth_router)

# Include tasks routes
api_router.include_router(tasks_router)

# Include other API routers here as needed

__all__ = ["api_router"]