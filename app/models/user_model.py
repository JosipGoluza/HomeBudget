from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=False)
    username = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(100), nullable=False, unique=False, index=False)

