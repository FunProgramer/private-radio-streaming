import random
import string

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from radiostation import crud, models, schemas
from radiostation.config import settings
from radiostation.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def check_len(var, var_name, max_len):
    if len(var) > max_len:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="The given {var} is too long. Max length: {max_length}, Length "
                                    "of given {var}: {given_length}"
                             .format(var=var_name,
                                     max_length=max_len,
                                     given_length=len(var))
                             )


@app.post("/sources/", response_model=schemas.Source, status_code=status.HTTP_201_CREATED)
def create_source(display_name: str, db: Session = Depends(get_db)):
    # Because we have no real upload for now use random file name str
    filename = get_random_string(10) + '.mp3'

    exception = check_len(display_name, "display_name", settings.max_str_length)
    if exception:
        raise exception
    exception = check_len(filename, "filename", settings.max_str_length)
    if exception:
        raise exception

    db_source = crud.get_source_by_filename(db, filename)
    if db_source:
        # Use 500 for non-real file upload (because then it is a server error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Source with filename '{}' already exists".format(filename))

    db_source = crud.get_source_by_display_name(db, display_name)
    if db_source:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Source with display_name '{}' already exists".format(display_name))
    return crud.create_source(db, display_name, filename)


@app.get("/sources/", response_model=list[schemas.Source])
def read_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sources(db, skip, limit)


@app.patch(path="/sources/{source_id}", response_model=schemas.Source)
def update_source(source_id: int, source: schemas.SourceUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_source(db, source, source_id)
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Source with id {} does not exist".format(source_id))


@app.delete(path="/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_source(db, source_id)
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Source with id {} does not exist".format(source_id))


@app.post("/channels/", response_model=schemas.Channel, status_code=status.HTTP_201_CREATED)
def create_channel(channel: schemas.ChannelCreate, db: Session = Depends(get_db)):
    exception = check_len(channel.stream_path, "stream_path", settings.max_str_length)
    if exception:
        raise exception

    db_source = crud.get_source(db, channel.source_id)
    if not db_source:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No source with source_id {} found".format(channel.source_id))

    db_channel = crud.get_channel_by_stream_path(db, channel.stream_path)
    if db_channel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Channel with stream_path '{}' already exists".format(channel.stream_path))

    created_channel = crud.create_channel(db, channel)
    channel_result = schemas.Channel(
        stream_path=created_channel.stream_path,
        source_id=created_channel.source_id,
        id=created_channel.id,
        pos=created_channel.pos,
        is_playing=False
    )
    return channel_result


@app.get("/channels/", response_model=list[schemas.Channel])
def read_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    channels = crud.get_channels(db, skip, limit)
    for channel in channels:
        channel.is_playing = False
    return channels


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
