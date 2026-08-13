from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .post import Post
    from .refreshtoken import RefreshToken
class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[bytes] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True, server_default='true')

    posts: Mapped[list['Post']] = relationship(back_populates='author')
    token: Mapped[list['RefreshToken']] = relationship(back_populates='user')
