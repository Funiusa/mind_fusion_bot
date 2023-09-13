from typing import List
from sqlalchemy.orm import Session
from fastapi import status, Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.api import deps, schemas, crud, models

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Message])
def get_messages(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
) -> List[schemas.Message]:
    messages = crud.message.get_multi_by_author(
        db=session, author_id=author_id, skip=skip, limit=limit
    )
    return messages


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
async def create_message(
    *,
    question: str,
    answer: str,
    author_id: int,
    session: Session = Depends(deps.get_session),
) -> schemas.Message:
    message_in = schemas.MessageCreate(question=question, answer=answer)
    message = crud.message.create_with_author(
        db=session, obj_in=message_in, author_id=author_id
    )
    return message


@router.put(
    "/{message_id}", status_code=status.HTTP_200_OK, response_model=schemas.Message
)
def update_message(
    *,
    message_id: int,
    message_in: schemas.MessageUpdate,
    session: Session = Depends(deps.get_session),
) -> schemas.Message:
    message = crud.message.get(db=session, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    updated_message = crud.message.update(session, db_obj=message, obj_in=message_in)
    return updated_message


@router.get(
    "/{message_id}", status_code=status.HTTP_200_OK, response_model=schemas.Message
)
def retrieve_message(
    *,
    message_id: int,
    session: Session = Depends(deps.get_session),
) -> schemas.Message:
    message = crud.message.get(session, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_message(
    *,
    message_id: int,
    session: Session = Depends(deps.get_session),
) -> None:
    post = crud.message.get(session, id=message_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    crud.message.remove(db=session, id=message_id)
