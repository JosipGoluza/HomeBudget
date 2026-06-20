from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers.auth_router import auth_router
from app.routers.user_router import user_router_v1

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router_v1)
app.include_router(auth_router)
