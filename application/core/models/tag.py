from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base
from .post_tag_association import  post_tag_association
if TYPE_CHECKING:
    from .post import Post
class Tag(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    posts: Mapped[list['Post']] = relationship(
        secondary=post_tag_association,
        back_populates='tags'
    )