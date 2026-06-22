from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.schemas.user_schema import UserCreate, UserOut
from app.services.user_service import create_user


class TestCreateUser:

    def test_returns_user_for_correct_body(self):
        user_create_body = UserCreate(
            username="test_username",
            email="test123@example.com",
            password="test_password123",
        )
        user_out_return = UserOut(
            id=1,
            username="test_username",
            email="test123@example.com",
            balance=0.0,
        )
        db = MagicMock()

        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "test_username"
        mock_user.email = "test123@example.com"
        mock_user.balance = 0.0

        with (
            patch("app.services.user_service.user_repository.get_by_email_or_username", return_value=None),
            patch("app.services.user_service.user_repository.add_user"),
            patch("app.services.user_service.get_password_hash", return_value="hashed"),
            patch("app.services.user_service.User", return_value=mock_user),
            patch("app.services.user_service.Categories"),
        ):
            assert create_user(db, user_create_body) == user_out_return

    def test_raises_when_email_or_username_taken(self):
        user_create_body = UserCreate(
            username="test_username",
            email="test123@example.com",
            password="test_password123",
        )

        with patch("app.services.user_service.user_repository.get_by_email_or_username", return_value=MagicMock()):
            with pytest.raises(HTTPException) as exc:
                create_user(db=MagicMock(), body=user_create_body)
            assert exc.value.status_code == 400

    def test_seeds_predefined_categories_on_registration(self):
        user_create_body = UserCreate(
            username="test_username",
            email="test123@example.com",
            password="test_password123",
        )
        db = MagicMock()

        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test123@example.com"
        mock_user.username = "test_username"
        mock_user.balance = Decimal("10000.00")

        with (
            patch("app.services.user_service.user_repository.get_by_email_or_username", return_value=None),
            patch("app.services.user_service.user_repository.add_user"),
            patch("app.services.user_service.get_password_hash", return_value="hashed"),
            patch("app.services.user_service.User", return_value=mock_user),
            patch("app.services.user_service.PREDEFINED_CATEGORIES", [("Food", "Daily food"), ("Travel", "Trips")]),
            patch("app.services.user_service.Categories"),
        ):
            create_user(db, user_create_body)

        assert db.add.call_count == 2