from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from app.dependencies import SessionDep
from app.models.user_model import User
from app.schemas.user_schema import UserOut, UserCreate
from app.utils.user import get_current_user

user_router_v1 = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

@user_router_v1.get("/me")
def get_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@user_router_v1.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "Email or username already exists"}},
)
def create_user(body: UserCreate, db: SessionDep):
    existing = db.query(User).filter(
        (User.email == body.email) | (User.username == body.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email or username already exists"
        )

    user = User(email=body.email, username=body.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
