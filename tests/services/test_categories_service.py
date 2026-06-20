from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.schemas.category_schema import CategoryCreate, CategoryGet
from app.services.category_service import create_category


class TestCreateCategory:

    def test_returns_category_instance_for_valid_input(self):
        category = CategoryCreate(name="Test Category", description="Test Category")
        db = MagicMock()
        user = MagicMock()

        mock_category = MagicMock()
        mock_category.id = 1
        mock_category.name = "Test Category"
        mock_category.description = "Test Category"

        with (
            patch("app.services.category_service.category_repository.get_category_by_name", return_value=None),
            patch("app.services.category_service.category_repository.add_category"),
            patch("app.services.category_service.Categories", return_value=mock_category),
        ):
            result = create_category(category, db, user)

        assert isinstance(result, CategoryGet)

    def test_raise_400_if_name_taken(self):
        category = CategoryCreate(name="Test Category", description="Test Category")
        db = MagicMock()
        user = MagicMock()

        with patch('app.services.category_service.category_repository.get_category_by_name', return_value=MagicMock()):
            with pytest.raises(HTTPException) as exc:
                create_category(category, db, user)

        assert exc.value.status_code == 400

    def test_returns_category_for_correct_body(self):
        category_body = CategoryCreate(name="Test Category", description="Test Category")
        category_response = CategoryGet(id=1, name="Test Category", description="Test Category")
        db = MagicMock()
        user = MagicMock()

        mock_category = MagicMock()
        mock_category.id = 1
        mock_category.name = "Test Category"
        mock_category.description = "Test Category"

        with (
            patch("app.services.category_service.category_repository.get_category_by_name", return_value=None),
            patch("app.services.category_service.category_repository.add_category"),
            patch("app.services.category_service.Categories", return_value=mock_category),
        ):
            result = create_category(category_body, db, user)

        assert result == category_response

    def test_links_category_to_user(self):
        category_body = CategoryCreate(name="Test Category", description="Test Category")
        db = MagicMock()
        user = MagicMock()

        mock_category = MagicMock()
        mock_category.id = 1
        mock_category.name = "Test Category"
        mock_category.description = "Test Category"

        with (
            patch('app.services.category_service.category_repository.get_category_by_name', return_value=None),
            patch("app.services.category_service.category_repository.add_category"),
            patch("app.services.category_service.Categories", return_value=mock_category),
        ):
            create_category(category_body, db, user)

        user.categories.append.assert_called_once_with(mock_category)