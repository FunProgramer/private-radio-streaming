# noinspection PyPackageRequirements
from pydantic import BaseModel


# Base Types include common values that are both used for reading and creation
class SourceBase(BaseModel):
    display_name: str


# This types (no postfix in the name) are used for reading
class Source(SourceBase):
    id: int
    filename: str

    class Config:
        from_attributes = True


class ChannelBase(BaseModel):
    stream_path: str
    source_id: int


# Create Types include values that are only needed for creation
class ChannelCreate(ChannelBase):
    pass


class Channel(ChannelBase):
    id: int
    pos: int
    is_playing: bool

    class Config:
        from_attributes = True
