from typing import Annotated
from sqlalchemy.orm.session import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database_connection import get_session

# Dependencies
# moved because of circular dependencies

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TokenDep = Annotated[str, Depends(oauth2_scheme)]

SessionDep = Annotated[Session, Depends(get_session)]

RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]