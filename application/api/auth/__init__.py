from fastapi import APIRouter
from .reg import router as reg_router
from core.config import settings

router = APIRouter(prefix=settings.api.auth.prefix, tags=["auth"])
router.include_router(reg_router)