from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import (
    create_expense,
    delete_expense,
    get_expense,
    get_expenses,
    update_expense,
)

FIXED_DATE = datetime(2026, 6, 20, 14, 30, tzinfo=timezone.utc)


def make_mock_expense(
        id_make: int = 1,
        amount: float = 49.99,
        description: str = "Test expense",
        date: datetime = FIXED_DATE,
        category_id: int = 1,
        user_id: int = 1,
):
    expense = MagicMock()
    expense.id = id_make
    expense.amount = Decimal(str(amount))
    expense.description = description
    expense.date = date
    expense.category_id = category_id
    expense.user_id = user_id
    return expense


def make_category(category_id=1, user_id=1):
    category = MagicMock()
    category.id = category_id
    category.user_id = user_id
    return category


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def user():
    u = MagicMock()
    u.id = 1
    u.balance = Decimal("1000.00")
    return u


class TestCreateExpense:

    def test_returns_expense_response_for_valid_input(self, db, user):
        body = ExpenseCreate(amount=49.99, category_id=1)
        mock_expense = make_mock_expense()

        with (
            patch("app.services.expense_service.category_repository.get_category_by_id", return_value=make_category()),
            patch("app.services.expense_service.expense_repository.add_expense"),
            patch("app.services.expense_service.Expense", return_value=mock_expense),
        ):
            result = create_expense(body, db, user)

        assert isinstance(result, ExpenseResponse)

    def test_returns_correct_expense_data(self, db, user):
        body = ExpenseCreate(amount=49.99, description="Groceries", category_id=1, date=FIXED_DATE)
        mock_expense = make_mock_expense(amount=49.99, description="Groceries", date=FIXED_DATE)
        expected = ExpenseResponse(id=1, amount=49.99, description="Groceries", date=FIXED_DATE, category_id=1)

        with (
            patch("app.services.expense_service.category_repository.get_category_by_id", return_value=make_category()),
            patch("app.services.expense_service.expense_repository.add_expense"),
            patch("app.services.expense_service.Expense", return_value=mock_expense),
        ):
            result = create_expense(body, db, user)

        assert result == expected

    def test_raises_404_if_category_not_found(self, db, user):
        body = ExpenseCreate(amount=49.99, category_id=99)

        with patch("app.services.expense_service.category_repository.get_category_by_id", return_value=None):
            with pytest.raises(HTTPException) as exc:
                create_expense(body, db, user)

        assert exc.value.status_code == 404

    def test_raises_404_if_category_belongs_to_another_user(self, db, user):
        body = ExpenseCreate(amount=49.99, category_id=1)

        with patch("app.services.expense_service.category_repository.get_category_by_id", return_value=make_category(user_id=2)):
            with pytest.raises(HTTPException) as exc:
                create_expense(body, db, user)

        assert exc.value.status_code == 404

    def test_defaults_date_to_now_when_not_provided(self, db, user):
        body = ExpenseCreate(amount=49.99, category_id=1)
        mock_expense = make_mock_expense()

        with (
            patch("app.services.expense_service.category_repository.get_category_by_id", return_value=make_category()),
            patch("app.services.expense_service.expense_repository.add_expense"),
            patch("app.services.expense_service.Expense", return_value=mock_expense),
        ):
            result = create_expense(body, db, user)

        assert result.date == mock_expense.date


class TestGetExpenses:

    def test_returns_list_of_expense_responses(self, db, user):
        with patch("app.services.expense_service.expense_repository.get_expenses", return_value=[make_mock_expense(
                id_make=1), make_mock_expense(id_make=2)]):
            result = get_expenses(db, user, None, None, None, None, None)

        assert len(result) == 2
        assert all(isinstance(expense, ExpenseResponse) for expense in result)

    def test_returns_empty_list_when_no_expenses(self, db, user):
        with patch("app.services.expense_service.expense_repository.get_expenses", return_value=[]):
            result = get_expenses(db, user, None, None, None, None, None)

        assert result == []

    def test_passes_all_filters_to_repository(self, db, user):
        with patch("app.services.expense_service.expense_repository.get_expenses", return_value=[]) as mock_repo:
            get_expenses(db, user, category_id=2, amount_min=10.0, amount_max=100.0, date_from=FIXED_DATE, date_to=FIXED_DATE)

        mock_repo.assert_called_once_with(user.id, db, 2, 10.0, 100.0, FIXED_DATE, FIXED_DATE)


class TestGetExpense:

    def test_returns_expense_response_for_valid_id(self, db, user):
        with patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=make_mock_expense()):
            result = get_expense(1, db, user)

        assert isinstance(result, ExpenseResponse)
        assert result.id == 1

    def test_raises_404_if_expense_not_found(self, db, user):
        with patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=None):
            with pytest.raises(HTTPException) as exc:
                get_expense(99, db, user)

        assert exc.value.status_code == 404


class TestUpdateExpense:

    def test_returns_updated_expense_response(self, db, user):
        body = ExpenseUpdate(amount=99.99)
        mock_expense = make_mock_expense(amount=99.99)

        with patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=mock_expense):
            result = update_expense(1, body, db, user)

        assert isinstance(result, ExpenseResponse)
        assert result.amount == Decimal("99.99")

    def test_raises_404_if_expense_not_found(self, db, user):
        body = ExpenseUpdate(amount=99.99)

        with patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=None):
            with pytest.raises(HTTPException) as exc:
                update_expense(99, body, db, user)

        assert exc.value.status_code == 404

    def test_raises_404_if_new_category_not_found(self, db, user):
        body = ExpenseUpdate(category_id=99)

        with (
            patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=make_mock_expense()),
            patch("app.services.expense_service.category_repository.get_category_by_id", return_value=None),
        ):
            with pytest.raises(HTTPException) as exc:
                update_expense(1, body, db, user)

        assert exc.value.status_code == 404

    def test_raises_404_if_new_category_belongs_to_another_user(self, db, user):
        body = ExpenseUpdate(category_id=2)

        with (
            patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=make_mock_expense()),
            patch("app.services.expense_service.category_repository.get_category_by_id", return_value=make_category(category_id=2, user_id=2)),
        ):
            with pytest.raises(HTTPException) as exc:
                update_expense(1, body, db, user)

        assert exc.value.status_code == 404

    def test_only_updates_provided_fields(self, db, user):
        body = ExpenseUpdate(amount=200.0)
        mock_expense = make_mock_expense(amount=49.99, description="Original", category_id=1)

        with patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=mock_expense):
            update_expense(1, body, db, user)

        assert mock_expense.amount == Decimal("200.0")
        assert mock_expense.description == "Original"
        assert mock_expense.category_id == 1


class TestDeleteExpense:

    def test_deletes_expense_and_commits(self, db, user):
        mock_expense = make_mock_expense()

        with (
            patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=mock_expense),
            patch("app.services.expense_service.expense_repository.delete_expense") as mock_delete,
        ):
            delete_expense(1, db, user)

        mock_delete.assert_called_once_with(db, mock_expense)
        db.commit.assert_called_once()

    def test_raises_404_if_expense_not_found(self, db, user):
        with patch("app.services.expense_service.expense_repository.get_expense_by_id", return_value=None):
            with pytest.raises(HTTPException) as exc:
                delete_expense(99, db, user)

        assert exc.value.status_code == 404
