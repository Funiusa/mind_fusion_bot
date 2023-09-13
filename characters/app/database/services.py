from sqlalchemy.orm import Session
from app.api import crud, schemas
from app.core.config import settings
from .base_class import Base
from .session import engine, SessionLocal


def init(db: Session) -> None:
    Base.metadata.create_all(engine)
    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER, name="Admin", surename="Admin"
        )
        user = crud.user.create(db, obj_in=user_in)


def init_db() -> None:
    db = SessionLocal()
    init(db)
