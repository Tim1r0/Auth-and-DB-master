from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User

from core.Schemas.User import UserCreate


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
async def get_user_by_id(
        session: AsyncSession,
        user_id: int,
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(
        session: AsyncSession,
        user_create: UserCreate,
        hashed_password: bytes
) -> User:
    new_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user