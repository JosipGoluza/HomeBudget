from typing import List

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=10000.0)

    categories: Mapped[List["Categories"]] = relationship(back_populates="user")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="user")
