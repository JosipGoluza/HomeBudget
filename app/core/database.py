import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, DeclarativeBase

metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    metadata = metadata_obj


database_url = os.getenv("DATABASE_URL", "")

engine = create_engine(
    database_url,
    echo=True,
    pool_size=5,
    pool_recycle=3600,
    max_overflow=10,
    pool_timeout=30,
)


def get_session():
    with Session(engine) as session:
        yield session
