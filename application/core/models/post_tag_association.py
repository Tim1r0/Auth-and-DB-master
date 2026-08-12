from sqlalchemy import Column, Table, ForeignKey
from .base import Base

post_tag_association = Table(
    'post_tag_association',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)