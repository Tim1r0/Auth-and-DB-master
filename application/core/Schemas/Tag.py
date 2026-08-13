from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str

class TagRead(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
