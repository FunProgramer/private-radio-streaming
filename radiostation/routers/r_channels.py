from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db

tag = "channels"
router = APIRouter()


@router.post("/channels/", tags=[tag], response_model=schemas.Channel, status_code=status.HTTP_201_CREATED)
def create_channel(channel: schemas.ChannelCreate, db: Session = Depends(get_db)):
    try:
        created_channel = crud.create_channel(db, channel)
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No source with source_id {} found".format(channel.source_id))
    except crud.DoesAlreadyExistException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Channel with stream_path '{}' already exists".format(channel.stream_path))

    return schemas.Channel(
        stream_path=created_channel.stream_path,
        source_id=created_channel.source_id,
        id=created_channel.id,
        pos=created_channel.pos,
        is_playing=False
    )


@router.get("/channels/", tags=[tag], response_model=list[schemas.Channel])
def read_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    channels = crud.get_channels(db, skip, limit)
    for channel in channels:
        channel.is_playing = False
    return channels


@router.patch(path="/channels/{channel_id}", tags=[tag], response_model=schemas.Channel)
def update_channel(channel_id: int, channel: schemas.ChannelUpdate, db: Session = Depends(get_db)):
    try:
        if channel.is_playing:
            channel.is_playing = None
        updated_channel = crud.update_channel(db, channel, channel_id)
        updated_channel.is_playing = False
        return updated_channel
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Channel with id {} does not exist".format(channel_id))


@router.delete(path="/channels/{channel_id}", tags=[tag], status_code=status.HTTP_204_NO_CONTENT)
def delete_source(channel_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_channel(db, channel_id)
    except crud.DoesNotExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Channel with id {} does not exist".format(channel_id))
