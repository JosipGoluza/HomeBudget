from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category_model import Categories
from app.models.user_model import User
from app.repositories import category_repository
from app.schemas.category_schema import CategoryCreate, CategoryCreated


def create_category(category_create: CategoryCreate, db: Session, user: User) -> CategoryCreated:
    if category_repository.get_category_by_name(category_create.name, db):
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Categories(
        name=category_create.name,
        description=category_create.description
    )

    category_repository.add_category(db, category)
    user.categories.append(category)
    db.commit()
    db.refresh(category)

    return CategoryCreated.model_validate(category)