from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from app.database.base_class import Base


class Character(Base):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[str] = mapped_column(index=True)
    content: Mapped[str] = mapped_column(unique=True, index=True)
    image: Mapped[str] = mapped_column(nullable=True)
