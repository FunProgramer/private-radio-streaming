from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
from .config import settings


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(settings.max_str_length), unique=True, nullable=False)
    filename = Column(String(settings.max_str_length), unique=True, nullable=False)


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    stream_path = Column(String(settings.max_str_length), unique=True, nullable=False)
    pos = Column(Integer, nullable=False)

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source")
