from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category_model import Categories
from app.models.user_model import User
from app.repositories import category_repository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse


def create_category(category_create: CategoryCreate, db: Session, user: User) -> CategoryResponse:
    if category_repository.get_category_by_name(category_create.name, user.id, db):
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Categories(
        name=category_create.name,
        description=category_create.description,
        user_id=user.id,
    )

    category_repository.add_category(db, category)
    db.commit()
    db.refresh(category)

    return CategoryResponse.model_validate(category)


def get_categories(db: Session, user: User) -> list[CategoryResponse]:
    categories = category_repository.get_categories(user.id, db)
    return [CategoryResponse.model_validate(c) for c in categories]


def get_category(category_id: int, db: Session, user: User) -> CategoryResponse:
    category = category_repository.get_category_by_id_user(category_id, user.id, db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryResponse.model_validate(category)


def update_category(category_id: int, body: CategoryUpdate, db: Session, user: User) -> CategoryResponse:
    category = category_repository.get_category_by_id_user(category_id, user.id, db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if body.name is not None:
        existing = category_repository.get_category_by_name(body.name, user.id, db)
        if existing and existing.id != category_id:
            raise HTTPException(status_code=400, detail="Category name already exists")
        category.name = body.name

    if body.description is not None:
        category.description = body.description

    db.commit()
    db.refresh(category)

    return CategoryResponse.model_validate(category)


def delete_category(category_id: int, db: Session, user: User) -> None:
    category = category_repository.get_category_by_id_user(category_id, user.id, db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category_repository.delete_category(db, category)
    db.commit()
