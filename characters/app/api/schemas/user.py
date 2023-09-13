from pydantic import BaseModel, Field
from datetime import datetime
from .message import Message


class UserBase(BaseModel):
    username: str = Field(default="example")
    name: str
    surename: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int | None = None
    time: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    messages: list[Message] = None


class UserInDB(UserInDBBase):
    pass
