from fastapi import APIRouter, status

from app.dependencies import SessionDep, CurrentUserDep
from app.schemas.category_schema import CategoryGet, CategoryCreate
from app.services import category_service

categories_router_v1 = APIRouter(
    prefix="/api/v1/categories",
    tags=["categories"],
)

@categories_router_v1.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryGet,
)
def categories_post_predefined(body: CategoryCreate, db: SessionDep, user: CurrentUserDep) -> CategoryGet:
    return category_service.create_category(body, db, user)