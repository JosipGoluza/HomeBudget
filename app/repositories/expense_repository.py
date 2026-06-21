from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.expense_model import Expense


def get_expense_by_id(expense_id: int, user_id: int, db: Session) -> Expense | None:
    return db.scalar(
        select(Expense).where(Expense.id == expense_id, Expense.user_id == user_id)
    )


def get_expenses(
    user_id: int,
    db: Session,
    category_id: int | None = None,
    amount_min: float | None = None,
    amount_max: float | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[Expense]:
    query = select(Expense).where(Expense.user_id == user_id)

    if category_id is not None:
        query = query.where(Expense.category_id == category_id)
    if amount_min is not None:
        query = query.where(Expense.amount >= amount_min)
    if amount_max is not None:
        query = query.where(Expense.amount <= amount_max)
    if date_from is not None:
        query = query.where(Expense.date >= date_from)
    if date_to is not None:
        query = query.where(Expense.date <= date_to)

    return list(db.scalars(query).all())


def get_expense_summary(
    user_id: int,
    date_from: datetime,
    date_to: datetime,
    db: Session,
    category_id: int | None = None,
) -> tuple[float, int]:
    query = (
        select(func.sum(Expense.amount), func.count(Expense.id))
        .where(Expense.user_id == user_id)
        .where(Expense.date >= date_from)
        .where(Expense.date <= date_to)
    )
    if category_id is not None:
        query = query.where(Expense.category_id == category_id)

    total, count = db.execute(query).one()

    return total if total is not None else 0.0, count if count is not None else 0


def add_expense(db: Session, expense: Expense) -> Expense:
    db.add(expense)
    db.flush()
    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
