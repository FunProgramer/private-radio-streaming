import random
import string
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.orm import Session

import crud
import schemas
from config import settings
from dependencies import get_db

router = APIRouter()


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@router.post("/sources/", response_model=schemas.Source, status_code=status.HTTP_201_CREATED)
def create_source(display_name: Annotated[str, Query(max_length=settings.max_str_length)],
                  db: Session = Depends(get_db)):
    # Because we have no real upload for now use random file name str
    filename = get_random_string(10) + '.mp3'

    if len(filename) > settings.max_str_length:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The given {var} is too long. Max length: {max_length}, Length "
                                   "of given {var}: {given_length}"
                            .format(var="filename",
                                    max_length=settings.max_str_length,
                                    given_length=len(filename))
                            )

    try:
        return crud.create_source(db, display_name, filename)
    except crud.DoesAlreadyExistException as e:
        if e.key_name == "filename":
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            value = filename
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            value = display_name

        raise HTTPException(status_code=status_code,
                            detail="Source with {} '{}' already exits".format(e.key_name, value))


@router.get("/sources/", response_model=list[schemas.Source])
def read_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sources(db, skip, limit)


@router.patch(path="/sources/{source_id}", response_model=schemas.Source)
def update_source(source_id: int, source: schemas.SourceUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_source(db, source, source_id)
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Source with id {} does not exist".format(source_id))


@router.delete(path="/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_source(db, source_id)
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Source with id {} does not exist".format(source_id))
