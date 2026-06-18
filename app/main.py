from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session

from app.database_connection import get_session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
