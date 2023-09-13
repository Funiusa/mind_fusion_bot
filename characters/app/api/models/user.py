from __future__ import annotations

from typing import TYPE_CHECKING, List
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .message import Message


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    surename: Mapped[str] = mapped_column(index=True, nullable=True)
    time: Mapped[datetime] = datetime.utcnow()

    messages: Mapped[List["Message"]] = relationship(cascade="all, delete-orphan")
