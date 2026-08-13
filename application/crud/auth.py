from datetime import datetime, timezone, timedelta

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import RefreshToken


async def save_refresh_token(
    session: AsyncSession,
    user_id: int,
    token: str,
    expire_days: int = 30
):
    expire_at = int((datetime.now(timezone.utc) + timedelta(days=expire_days)).timestamp())
    new_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expire_at
    )
    session.add(new_token)
    await session.commit()

async def get_refresh_token(
    session: AsyncSession,
    token: str
) -> RefreshToken | None:
    now = int(datetime.now(timezone.utc).timestamp())
    stmt = select(RefreshToken).where(
        RefreshToken.token == token,
        RefreshToken.expires_at > now
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def delete_refresh_token(
        session: AsyncSession,
        token: str,
):
    stmt = delete(RefreshToken).where(RefreshToken.token == token)
    await session.execute(stmt)
    await session.commit()

