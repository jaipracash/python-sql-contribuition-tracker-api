from fastapi import APIRouter
from src.endpoints.user import router as user_router
from src.endpoints.events import router as event_router
from src.endpoints.contributions import router as contribution_router

router = APIRouter()

router.include_router(user_router)
router.include_router(event_router)
router.include_router(contribution_router)
