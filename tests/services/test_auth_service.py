from datetime import timedelta, datetime, timezone
from unittest.mock import MagicMock, patch

import jwt
import pytest
from fastapi import HTTPException

from app.models.user_model import User
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)


@pytest.fixture
def secret_key():
    with (patch("app.services.auth_service.SECRET_KEY", "test-secret-type-until-32-to-remove-warning"),
          patch("app.services.auth_service.ALGORITHM", "HS256")):
        yield "test-secret-type-until-32-to-remove-warning"


class TestVerifyPassword:
    def test_returns_true_for_correct_password(self):
        hashed = get_password_hash("mypassword")
        assert verify_password("mypassword", hashed) is True

    def test_returns_false_for_wrong_password(self):
        hashed = get_password_hash("mypassword")
        assert verify_password("wrongpassword", hashed) is False


class TestGetPasswordHash:
    def test_returns_string(self):
        assert isinstance(get_password_hash("mypassword"), str)


class TestAuthenticateUser:
    def test_returns_none_when_user_not_found(self):
        db = MagicMock()
        with (patch("app.services.auth_service.user_repository.get_by_username", return_value=None),
              patch("app.services.auth_service.verify_password") as mock_verify
              ):
            assert authenticate_user(db, "nonexistent", "password") is None
        mock_verify.assert_called_once()

    def test_returns_none_when_password_incorrect(self):
        db = MagicMock()
        user = User(username="testuser", hashed_password=get_password_hash("correctpassword"))
        with patch("app.services.auth_service.user_repository.get_by_username", return_value=user):
            assert authenticate_user(db, "testuser", "wrongpassword") is None

    def test_returns_user_when_credentials_are_valid(self):
        db = MagicMock()
        user = User(username="testuser", hashed_password=get_password_hash("correctpassword"))
        with patch("app.services.auth_service.user_repository.get_by_username", return_value=user):
            assert authenticate_user(db, "testuser", "correctpassword") is user


class TestCreateAccessToken:
    def test_creates_decodable_jwt_with_expected_claims(self, secret_key):
        token = create_access_token({"sub": "testuser"})
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert payload["sub"] == "testuser" and "exp" in payload

    def test_respects_custom_expires_delta(self, secret_key):
        token = create_access_token({"sub": "testuser"}, expires_delta=timedelta(hours=2))
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        remaining = (exp - datetime.now(timezone.utc)).total_seconds()
        assert remaining > 3600


class TestGetCurrentUser:
    def test_raises_401_for_invalid_token(self, secret_key):
        db = MagicMock()
        with pytest.raises(HTTPException) as exc:
            get_current_user("not-a-valid-token", db)
        assert exc.value.status_code == 401

    def test_raises_401_when_token_missing_sub(self, secret_key):
        db = MagicMock()
        token = jwt.encode({"data": "no_sub_here"}, secret_key, algorithm="HS256")
        with pytest.raises(HTTPException) as exc:
            get_current_user(token, db)
        assert exc.value.status_code == 401

    def test_raises_401_when_user_not_found_in_db(self, secret_key):
        db = MagicMock()
        token = create_access_token({"sub": "nonexistent"})
        with (patch("app.services.auth_service.user_repository.get_by_username", return_value=None),
              pytest.raises(HTTPException) as exc):
            get_current_user(token, db)
        assert exc.value.status_code == 401

    def test_returns_user_for_valid_token(self, secret_key):
        db = MagicMock()
        user = User(username="testuser")
        token = create_access_token({"sub": "testuser"})
        with patch("app.services.auth_service.user_repository.get_by_username", return_value=user):
            assert get_current_user(token, db) is user
