from fastapi import APIRouter
from .tasks import router as tasks_router

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Include tasks routes
router.include_router(tasks_router)