from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.expense_model import Expense
from app.models.user_model import User
from app.repositories import category_repository, expense_repository
from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse, ExpenseUpdate


def create_expense(body: ExpenseCreate, db: Session, user: User) -> ExpenseResponse:
    category = category_repository.get_category_by_id(body.category_id, db)
    if not category or category.user_id != user.id:
        raise HTTPException(status_code=404, detail="Category not found")

    expense = Expense(
        amount=body.amount,
        description=body.description,
        date=body.date if body.date is not None else datetime.now(timezone.utc),
        category_id=body.category_id,
        user_id=user.id,
    )

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

    expense_repository.delete_expense(db, expense)
    db.commit()
