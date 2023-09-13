from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.types import BigInteger
from .base import CRUDBase
from app.api.models.character import Character
from app.api.schemas.character import CharacterCreate, CharacterUpdate

from typing import Union, Any, Dict


class CRUDCharacter(CRUDBase[Character, CharacterCreate, CharacterUpdate]):
    @staticmethod
    def get_by_name(db: Session, *, name: str) -> Optional[Character]:
        stmt = select(Character).filter_by(name=name)
        return db.execute(statement=stmt).scalars().first()


character = CRUDCharacter(Character)
