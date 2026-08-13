from datetime import datetime, timezone, timedelta

from sqlalchemy import select
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
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

