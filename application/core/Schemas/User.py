import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    is_active: bool