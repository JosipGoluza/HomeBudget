from fastapi import FastAPI, HTTPException, status

from app.database_connection import Base, engine
from app.dependencies import SessionDep, RequestFormDep
from app.models.user_model import User
from app.routers.user_route import user_router_v1

Base.metadata.create_all(engine)

app = FastAPI()


@app.post(
    "/token",
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "Incorrect username or password"}},
)
def login(form_data: RequestFormDep, db: SessionDep):
    user_dict = db.query(User).filter((User.username == form_data.username)).first()
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"token": "token"}


app.include_router(user_router_v1)
