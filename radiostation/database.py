from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from radiostation.config import settings

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/radiostation".format(
    settings.db_user, settings.db_password, settings.db_server
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
