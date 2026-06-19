from typing import Annotated

from fastapi import Depends

from app.dependencies import oauth2_scheme, SessionDep
from app.models.user_model import User


def get_current_user(db: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    user = db.get(User, 1)
    return user
