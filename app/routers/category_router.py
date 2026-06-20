from fastapi import APIRouter, status

from app.dependencies import SessionDep, CurrentUserDep
from app.schemas.category_schema import CategoryCreated, CategoryCreate
from app.services import category_service

categories_router_v1 = APIRouter(
    prefix="/api/v1/categories",
    tags=["categories"],
)

@categories_router_v1.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryCreated,
    responses={
        201: {
            "description": "Category successfully created",
            "model": CategoryCreated
        },
        400: {
            "description": "Invalid request - missing or invalid category name"
        },
        401: {
            "description": "Unauthorized - missing or invalid authentication token"
        },
        422: {
            "description": "Validation error - request body format is invalid"
        }
    }
)
def categories_post_predefined(body: CategoryCreate, db: SessionDep, user: CurrentUserDep) -> CategoryCreated:
    """
    Create a new expense category for the authenticated user.

    **Request body:**
    - `name`: Category name (3-50 characters, required)
    - `description`: Optional category description (3-50 characters)
    """
    return category_service.create_category(body, db, user)