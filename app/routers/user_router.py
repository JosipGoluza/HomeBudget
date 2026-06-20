from fastapi import APIRouter, status

from app.dependencies import SessionDep, CurrentUserDep
from app.schemas.user_schema import UserOut, UserCreate
from app.services import user_service

user_router_v1 = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@user_router_v1.get("/me", response_model=UserOut)
def get_me(current_user: CurrentUserDep):
    return current_user


@user_router_v1.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "Email or username already exists"}},
)
def create_user(body: UserCreate, db: SessionDep):
    return user_service.create_user(db, body)
