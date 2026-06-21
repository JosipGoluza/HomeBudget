from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.expense_model import Expense
from app.models.user_model import User
from app.repositories import category_repository, expense_repository
from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse, ExpenseSummaryResponse, ExpenseUpdate
from app.utils.date_utils import resolve_period


def create_expense(body: ExpenseCreate, db: Session, user: User) -> ExpenseResponse:
    category = category_repository.get_category_by_id(body.category_id, db)
    if not category or category.user_id != user.id:
        raise HTTPException(status_code=404, detail="Category not found")

    if user.balance < body.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    expense = Expense(
        amount=body.amount,
        description=body.description,
        date=body.date if body.date is not None else datetime.now(timezone.utc),
        category_id=body.category_id,
        user_id=user.id,
    )

    user.balance -= body.amount
    expense_repository.add_expense(db, expense)
    db.commit()
    db.refresh(expense)

    return ExpenseResponse.model_validate(expense)


def get_expenses(
    db: Session,
    user: User,
    category_id: int | None,
    amount_min: float | None,
    amount_max: float | None,
    date_from: datetime | None,
    date_to: datetime | None,
) -> list[ExpenseResponse]:
    expenses = expense_repository.get_expenses(
        user.id, db, category_id, amount_min, amount_max, date_from, date_to
    )
    return [ExpenseResponse.model_validate(expense) for expense in expenses]


def get_expense(expense_id: int, db: Session, user: User) -> ExpenseResponse:
    expense = expense_repository.get_expense_by_id(expense_id, user.id, db)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return ExpenseResponse.model_validate(expense)


def update_expense(expense_id: int, body: ExpenseUpdate, db: Session, user: User) -> ExpenseResponse:
    expense = expense_repository.get_expense_by_id(expense_id, user.id, db)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if body.category_id is not None:
        category = category_repository.get_category_by_id(body.category_id, db)
        if not category or category.user_id != user.id:
            raise HTTPException(status_code=404, detail="Category not found")
        expense.category_id = body.category_id

    if body.amount is not None:
        expense.amount = body.amount
    if body.description is not None:
        expense.description = body.description
    if body.date is not None:
        expense.date = body.date

    db.commit()
    db.refresh(expense)

    return ExpenseResponse.model_validate(expense)


def delete_expense(expense_id: int, db: Session, user: User) -> None:
    expense = expense_repository.get_expense_by_id(expense_id, user.id, db)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    user.balance += expense.amount
    expense_repository.delete_expense(db, expense)
    db.commit()


def get_expense_summary(
    db: Session,
    user: User,
    period: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
    category_id: int | None,
) -> ExpenseSummaryResponse:

    if period and (date_from or date_to):
        raise HTTPException(status_code=400, detail="Provide either 'period' or 'date_from'/'date_to', not both")
    if not period and (not date_from and not date_to):
        raise HTTPException(status_code=400, detail="Provide either 'period' or 'date_from'/'date_to'")
    if date_from and not date_to or not date_from and date_to :
        raise HTTPException(status_code=400, detail="Both 'date_from' and 'date_to' are required for custom range")

    if period:
        date_from, date_to = resolve_period(period)


    if category_id is not None:
        category = category_repository.get_category_by_id(category_id, db)
        if not category or category.user_id != user.id:
            raise HTTPException(status_code=404, detail="Category not found")

    total, count = expense_repository.get_expense_summary(user.id, date_from, date_to, db, category_id)

    return ExpenseSummaryResponse(
        total=total,
        count=count,
        period_from=date_from,
        period_to=date_to,
        category_id=category_id,
    )
