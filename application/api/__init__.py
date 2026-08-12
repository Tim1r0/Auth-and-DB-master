from fastapi import APIRouter

from core.config import settings

api_router = APIRouter(
    prefix=settings.api.prefix
)