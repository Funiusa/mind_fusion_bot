from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from .base import CRUDBase
from app.api.models.message import Message
from app.api.schemas.message import MessageCreate, MessageUpdate


class CRUDPost(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: MessageCreate, author_id: int
    ) -> Message:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        stmt = (
            select(self.model).filter_by(author_id=author_id).offset(skip).limit(limit)
        )
        return db.execute(statement=stmt).scalars().all()

    def get_message_by_author(self, db: Session, *, author_id: int) -> Message:
        stmt = (
            select(self.model)
            .filter_by(author_id=author_id)
            .order_by(self.model.id.desc())
        )
        return db.execute(statement=stmt).scalars().first()


message = CRUDPost(Message)
