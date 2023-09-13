import shutil
from typing import List, Any
from fastapi import Depends, status, Body, UploadFile
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api import schemas, models, crud, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Character])
async def get_characters(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
) -> list[schemas.Character]:
    characters = crud.character.get_multi(db=session, skip=skip, limit=limit)
    return characters


@router.post("/")
def create_character(
    *,
    name: str,
    role: str,
    content: str,
    image: UploadFile,
    session: Session = Depends(deps.get_session),
) -> Any:
    try:
        image_path = "./static/images/" + image.filename
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        char_in = schemas.CharacterCreate(
            name=name, role=role, content=content, image=image_path
        )
        character = crud.character.create(db=session, obj_in=char_in)
        return character
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Fields must be unique",
        )


@router.get("/{char_id}", response_model=schemas.Character)
def get_character_by_id(
    char_id: int,
    session: Session = Depends(deps.get_session),
) -> schemas.Character:
    character = crud.character.get(db=session, id=char_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The character doesn't exists",
        )
    return character


@router.put("/{char_id}", response_model=schemas.Character)
def update_character(
    char_id: int,
    char_in: schemas.CharacterUpdate,
    session: Session = Depends(deps.get_session),
) -> schemas.Character:
    character = crud.character.get(db=session, id=char_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character doesn't exists"
        )
    updated_char = crud.character.update(session, db_obj=character, obj_in=char_in)
    return updated_char


@router.delete("/{char_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_character(
    char_id: int,
    session: Session = Depends(deps.get_session),
) -> None:
    character = crud.char.get(db=session, id=char_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character doesn't exists"
        )
    crud.character.remove(db=session, id=char_id)
