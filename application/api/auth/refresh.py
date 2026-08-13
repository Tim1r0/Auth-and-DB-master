from datetime import timedelta

from fastapi import APIRouter, Cookie, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import decode_jwt, encode_jwt
from core.config import settings
from core.models import db_helper
from crud.auth import get_refresh_token
router = APIRouter()

@router.post("/refresh")
async def refresh(
        refresh_token: str | None = Cookie(None),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No refresh token'
        )
    try:
        payload = decode_jwt(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token'
        )

    if payload.get('type') != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token type'
        )

    db_token = await get_refresh_token(session, refresh_token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token not founded'
        )

    user_id = payload.get('sub')

    new_access_token = encode_jwt(
        payload={
            'sub': user_id,
            'type': 'access'
        },
        expire_timedelta=timedelta(minutes=settings.auth_jwt.access_token_expires_min)
    )

    return {
        'access_token': new_access_token,
        'token_type': 'bearer'
    }