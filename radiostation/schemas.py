from typing import Annotated

from fastapi import Query
# noinspection PyPackageRequirements
from pydantic import BaseModel

from config import settings


# Base Types include common values that are both used for reading and creation
class SourceBase(BaseModel):
    display_name: Annotated[str, Query(max_length=settings.max_str_length)]


# This types (no postfix in the name) are used for reading
class Source(SourceBase):
    id: int
    filename: Annotated[str, Query(max_length=settings.max_str_length)]

    class Config:
        from_attributes = True


# The Update Types are used for updating multiple or single specific attributes
class SourceUpdate(BaseModel):
    display_name: Annotated[str | None, Query(max_length=settings.max_str_length)] = None
    filename: Annotated[str | None, Query(max_length=settings.max_str_length)] = None


class ChannelBase(BaseModel):
    stream_path: Annotated[str, Query(max_length=settings.max_str_length)]
    source_id: int | None


# Create Types include values that are only needed for creation
class ChannelCreate(ChannelBase):
    pass


class Channel(ChannelBase):
    id: int
    pos: int
    is_playing: bool

    class Config:
        from_attributes = True


class ChannelUpdate(BaseModel):
    stream_path: Annotated[str | None, Query(max_length=settings.max_str_length)] = None
    source_id: int | None = None
    pos: int | None = None
    is_playing: bool | None = None
