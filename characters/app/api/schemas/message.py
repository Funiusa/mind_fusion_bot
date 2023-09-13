from datetime import datetime

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    question: str = Field(default="How do you do?")
    answer: str = Field(default="Fine. Thanks!")


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: int
    question: str
    answer: str
    author_id: int
    creation_date: datetime

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    pass


class MessageInDB(MessageInDBBase):
    pass
