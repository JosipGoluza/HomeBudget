from fastapi import APIRouter, status

from app.dependencies import SessionDep, CurrentUserDep
from app.schemas.user_schema import UserOut, UserCreate
from app.services import user_service

user_router_v1 = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@user_router_v1.get(
    "/me",
    response_model=UserOut,
    responses={
        200: {
            "description": "Current user profile retrieved successfully",
            "model": UserOut
        },
        401: {
            "description": "Unauthorized - missing or invalid authentication token"
        }
    }
)
def get_me(current_user: CurrentUserDep):
    """
    Get the profile of the currently authenticated user.

    This endpoint requires a valid JWT token in the Authorization header
    (format: `Bearer <token>`). Returns the authenticated user's account details.

    """
    return current_user


@user_router_v1.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User account successfully created",
            "model": UserOut
        },
        400: {
            "description": "Invalid request - validation failed"
        },
        409: {
            "description": "Conflict - username or email already registered"
        },
        422: {
            "description": "Validation error - request body format is invalid"
        }
    }
)
def create_user(body: UserCreate, db: SessionDep):
    """
    Create a new user account.

    Username and email must be unique. Password must be at least 12 characters.

    **Request body:**
    - `username`: Unique username (3-50 characters)
    - `email`: Valid email address
    - `password`: Account password (12+ characters)
    """
    return user_service.create_user(db, body)
