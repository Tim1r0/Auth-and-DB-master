from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base
from .post_tag_association import post_tag_association
if TYPE_CHECKING:
    from .user import User
    from .tag import Tag
class Post(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    author: Mapped['User'] = relationship(back_populates='posts')
    tags: Mapped[list['Tag']] = relationship(
        secondary=post_tag_association,
        back_populates='posts'
    )
