from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.types import BigInteger
from .base import CRUDBase
from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate

from typing import Union, Any, Dict


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def get_by_username(db: Session, *, username: str) -> Optional[User]:
        stmt = select(User).filter_by(username=username)
        return db.execute(statement=stmt).scalars().first()


user = CRUDUser(User)
