from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth import check_password
from auth.utils import hash_password, create_tokens
from core.config import settings
from core.models import db_helper
from crud import save_refresh_token, get_user_by_email

router = APIRouter(
    tags=['auth'],
)

@router.post('/login')
async def login(
    response: Response,
    from_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user = await get_user_by_email(email=from_data.username, session=session)
    if not user or not check_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access, refresh = create_tokens(user_id=user.id, email=user.email)

    await save_refresh_token(session=session, user_id=user.id, token=refresh)

    response.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True,
        secure=False,
        samesite='lax',
    )

    return {
        'access_token': access,
        'token_type': 'bearer',
    }




