from fastapi import APIRouter
from core.config import settings
from .reg import router as reg_router
from .login import router as login_router

router = APIRouter(prefix=settings.api.auth.prefix, tags=["auth"])
router.include_router(reg_router)
router.include_router(login_router)