from sqlalchemy.orm import Session

from . import models, schemas


class DoesNotExistException(Exception):
    pass


def get_source(db: Session, source_id: int):
    return db.query(models.Source).filter(models.Source.id == source_id).first()


def get_source_by_filename(db: Session, filename: str):
    return db.query(models.Source).filter(models.Source.filename == filename).first()


def get_source_by_display_name(db: Session, display_name: str):
    return db.query(models.Source).filter(models.Source.display_name == display_name).first()


def get_sources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Source).offset(skip).limit(limit).all()


def create_source(db: Session, display_name: str, filename: str):
    db_source = models.Source(display_name=display_name, filename=filename)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def update_source(db: Session, source: schemas.SourceUpdate, source_id: int):
    db_source = get_source(db, source_id)
    if not db_source:
        raise DoesNotExistException()
    source_data = source.model_dump(exclude_unset=True)
    for key, value in source_data.items():
        setattr(db_source, key, value)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_channels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Channel).offset(skip).limit(limit).all()


def get_channel_by_stream_path(db: Session, stream_path: str):
    return db.query(models.Channel).filter(models.Channel.stream_path == stream_path).first()


def create_channel(db: Session, channel: schemas.ChannelCreate):
    db_channel = models.Channel(**channel.model_dump(), pos=0)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel
