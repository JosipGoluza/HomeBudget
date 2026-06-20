from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers.auth_router import auth_router
from app.routers.category_router import categories_router_v1
from app.routers.expense_router import expenses_router_v1
from app.routers.user_router import user_router_v1

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router_v1)
app.include_router(auth_router)
app.include_router(categories_router_v1)
app.include_router(expenses_router_v1)