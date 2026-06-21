from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import RequestFormDep, SessionDep
from app.schemas.user_schema import Token
from app.services import auth_service

auth_router = APIRouter(
    prefix="",
    tags=["auth"],
)


@auth_router.post(
    "/token",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    responses={
        201: {"description": "Authentication successful, JWT token created","model": Token},
        400: {"description": "Invalid request body - username and password fields are required"},
        401: {"description": "Unauthorized - invalid username or password combination"},
        422: {"description": "Validation error - request body format is invalid"}
    }
)
def login(form_data: RequestFormDep, db: SessionDep):
    """
    Authenticate user and return JWT access token.

    **Request:** Form data with `username` and `password` fields

    **Returns:** JWT token with configurable expiration time

    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")
