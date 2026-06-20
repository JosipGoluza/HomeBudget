from datetime import datetime

from fastapi import APIRouter, Query, status

from app.dependencies import CurrentUserDep, SessionDep
from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services import expense_service

expenses_router_v1 = APIRouter(
    prefix="/api/v1/expenses",
    tags=["expenses"],
)


@expenses_router_v1.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponse,
    responses={
        201: {"description": "Expense successfully created", "model": ExpenseResponse},
        400: {"description": "Invalid request body"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Category not found"},
        422: {"description": "Validation error - request body format is invalid"},
    },
)
def create_expense(body: ExpenseCreate, db: SessionDep, user: CurrentUserDep) -> ExpenseResponse:
    """
    Create a new expense for the authenticated user.

    **Request body:**
    - `amount`: Amount spent, must be greater than 0 (required)
    - `category_id`: ID of an existing category belonging to the user (required)
    - `description`: Optional description (3-255 characters)
    - `date`: Optional datetime, defaults to now
    """
    return expense_service.create_expense(body, db, user)


@expenses_router_v1.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseResponse],
    responses={
        200: {"description": "List of expenses matching the filters"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
    },
)
def list_expenses(
    db: SessionDep,
    user: CurrentUserDep,
    category_id: int | None = Query(default=None, description="Filter by category ID"),
    amount_min: float | None = Query(default=None, description="Minimum amount (inclusive)", gt=0),
    amount_max: float | None = Query(default=None, description="Maximum amount (inclusive)", gt=0),
    date_from: datetime | None = Query(default=None, description="Filter expenses on or after this date"),
    date_to: datetime | None = Query(default=None, description="Filter expenses on or before this date"),
) -> list[ExpenseResponse]:
    """
    List all expenses for the authenticated user, with optional filters.

    **Query parameters (all optional):**
    - `category_id`: Filter by category
    - `amount_min` / `amount_max`: Filter by price range
    - `date_from` / `date_to`: Filter by date range
    """
    return expense_service.get_expenses(db, user, category_id, amount_min, amount_max, date_from, date_to)


@expenses_router_v1.get(
    "/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponse,
    responses={
        200: {"description": "Expense details", "model": ExpenseResponse},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Expense not found"},
    },
)
def get_expense(expense_id: int, db: SessionDep, user: CurrentUserDep) -> ExpenseResponse:
    """Get a single expense by ID. Only returns expenses belonging to the authenticated user."""
    return expense_service.get_expense(expense_id, db, user)


@expenses_router_v1.put(
    "/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponse,
    responses={
        200: {"description": "Expense successfully updated", "model": ExpenseResponse},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Expense not found"},
        422: {"description": "Validation error - request body format is invalid"},
    },
)
def update_expense(expense_id: int, body: ExpenseUpdate, db: SessionDep, user: CurrentUserDep) -> ExpenseResponse:
    """
    Update an existing expense. All fields are optional — only provided fields are updated.
    """
    return expense_service.update_expense(expense_id, body, db, user)


@expenses_router_v1.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Expense successfully deleted"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Expense not found"},
    },
)
def delete_expense(expense_id: int, db: SessionDep, user: CurrentUserDep) -> None:
    """Delete an expense by ID. Only the owner can delete their expense."""
    expense_service.delete_expense(expense_id, db, user)
