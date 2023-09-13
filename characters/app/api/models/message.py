from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question: Mapped[str] = mapped_column(nullable=True)
    answer: Mapped[str] = mapped_column(nullable=True)
    creation_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    author: Mapped["User"] = relationship(back_populates="messages")
