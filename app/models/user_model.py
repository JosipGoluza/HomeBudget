from decimal import Decimal
from typing import List

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("10000.00"))

    categories: Mapped[List["Categories"]] = relationship(back_populates="user")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="user")
