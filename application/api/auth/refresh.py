from datetime import timedelta

from fastapi import APIRouter, Cookie, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth import create_tokens
from auth.utils import decode_jwt
from core.models import db_helper
from crud.auth import get_refresh_token, delete_refresh_token
from crud.user import get_user_by_id
router = APIRouter()

@router.post("/refresh")
async def refresh(
        response: Response,
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
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )
    await delete_refresh_token(session, refresh_token)

    access_new, refresh_new = create_tokens(user_id=user_id, email=user.email)
    response.set_cookie(
        key='refresh_token',
        value=refresh_new,
        httponly=True,
    )
    return {
        'access_token': access_new,
        'token_type': 'bearer'
    }