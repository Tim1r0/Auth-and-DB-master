from fastapi import APIRouter

from core.config import settings
from .auth import router as auth_router

api_router = APIRouter(
    prefix=settings.api.prefix
)
api_router.include_router(auth_router)