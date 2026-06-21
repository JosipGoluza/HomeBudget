from fastapi import APIRouter, status

from app.dependencies import SessionDep, CurrentUserDep
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import category_service

categories_router_v1 = APIRouter(
    prefix="/api/v1/categories",
    tags=["categories"],
)


@categories_router_v1.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
    responses={
        201: {"description": "Category successfully created", "model": CategoryResponse},
        400: {"description": "Category name already exists"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        422: {"description": "Validation error - request body format is invalid"},
    },
)
def create_category(body: CategoryCreate, db: SessionDep, user: CurrentUserDep) -> CategoryResponse:
    """
    Create a new expense category for the authenticated user.

    **Request body:**
    - `name`: Category name (3-50 characters, required)
    - `description`: Optional category description (3-50 characters)
    """
    return category_service.create_category(body, db, user)


@categories_router_v1.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryResponse],
    responses={
        200: {"description": "List of categories for the authenticated user"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
    },
)
def list_categories(db: SessionDep, user: CurrentUserDep) -> list[CategoryResponse]:
    """List all categories belonging to the authenticated user."""
    return category_service.get_categories(db, user)


@categories_router_v1.get(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
        200: {"description": "Category details", "model": CategoryResponse},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Category not found"},
    },
)
def get_category(category_id: int, db: SessionDep, user: CurrentUserDep) -> CategoryResponse:
    """Get a single category by ID. Only returns categories belonging to the authenticated user."""
    return category_service.get_category(category_id, db, user)


@categories_router_v1.put(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
        200: {"description": "Category successfully updated", "model": CategoryResponse},
        400: {"description": "Category name already exists"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Category not found"},
        422: {"description": "Validation error - request body format is invalid"},
    },
)
def update_category(category_id: int, body: CategoryUpdate, db: SessionDep, user: CurrentUserDep) -> CategoryResponse:
    """
    Update an existing category. All fields are optional — only provided fields are updated.
    """
    return category_service.update_category(category_id, body, db, user)


@categories_router_v1.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Category successfully deleted (expenses also deleted)"},
        401: {"description": "Unauthorized - missing or invalid authentication token"},
        404: {"description": "Category not found"},
    },
)
def delete_category(category_id: int, db: SessionDep, user: CurrentUserDep) -> None:
    """Delete a category by ID. All expenses belonging to this category are also deleted."""
    category_service.delete_category(category_id, db, user)
