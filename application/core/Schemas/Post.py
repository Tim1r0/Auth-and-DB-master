from pydantic import BaseModel, ConfigDict

from core.Schemas.Tag import TagRead


class Post(BaseModel):
    title: str

class PostCreate(Post):

    tag_id: list[int]

class PostRead(Post):
    id: int
    author_id: int
    tags: list[TagRead]
    model_config = ConfigDict(from_attributes=True)
