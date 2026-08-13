from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import hash_password
from core.Schemas import UserRead, UserCreate
from core.config import settings
from core.models import db_helper
from crud import get_user_by_email, create_user

router = APIRouter(
    prefix=settings.api.auth.register_path,
)

@router.post('', response_model=UserRead)
async def register_user(
        user_in: UserCreate,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    find_user = await get_user_by_email(session=session, email=user_in.email)
    if find_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already registered',
        )
    hash_pwd = hash_password(user_in.password)
    new_user = await create_user(
        session=session,
        user_create=user_in,
        hashed_password=hash_pwd,
    )
    return new_user

