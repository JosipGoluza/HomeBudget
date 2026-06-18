from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

def get_session():
    with Session(engine) as session:
        yield session


database_url = os.getenv("DATABASE_URL", "")
print(database_url)

engine = create_engine(database_url, echo=True, pool_size=5, pool_recycle=3600, max_overflow=10, pool_timeout=30)
