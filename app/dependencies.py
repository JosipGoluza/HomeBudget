from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.user_model import User
from app.services.auth_service import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]
SessionDep = Annotated[Session, Depends(get_session)]
RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_current_user_dep(token: TokenDep, db: SessionDep) -> User:
    return get_current_user(token, db)


CurrentUserDep = Annotated[User, Depends(get_current_user_dep)]
