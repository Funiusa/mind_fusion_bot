from typing import List, Any
from fastapi import Depends, status, Body
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import schemas, models, crud, deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
) -> list[schemas.User]:
    users = crud.user.get_multi(db=session, skip=skip, limit=limit)
    return users


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    session: Session = Depends(deps.get_session),
    user_in: schemas.UserCreate,
) -> Any:
    user = crud.user.create(db=session, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(
    user_id: int,
    session: Session = Depends(deps.get_session),
) -> schemas.User:
    user = crud.user.get(db=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't exists",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user_by_id(
    user_id: int,
    user_in: schemas.UserUpdate,
    session: Session = Depends(deps.get_session),
) -> schemas.User:
    user = crud.user.get(db=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists"
        )
    updated_user = crud.user.update(session, db_obj=user, obj_in=user_in)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int,
    session: Session = Depends(deps.get_session),
) -> None:
    user = crud.user.get(db=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists"
        )
    if user.username == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A Dutchman must always have a captain",
        )
    crud.user.remove(db=session, id=user_id)
