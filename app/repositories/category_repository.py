from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category_model import Categories


def get_category_by_id(category_id: int, db: Session) -> Categories | None:
    return db.scalar(select(Categories).where(Categories.id == category_id))

def get_category_by_name(category_name: str, user_id: int, db: Session) -> Categories | None:
    return db.scalar(
        select(Categories).where(Categories.name == category_name, Categories.user_id == user_id)
    )

def get_category_by_id_user(category_id: int, user_id: int, db: Session) -> Categories | None:
    return db.scalar(
        select(Categories).where(Categories.id == category_id, Categories.user_id == user_id)
    )

def get_categories(user_id: int, db: Session) -> list[Categories]:
    return list(db.scalars(select(Categories).where(Categories.user_id == user_id)).all())

def add_category(db: Session, category: Categories) -> Categories:
    db.add(category)
    db.flush()
    return category

def delete_category(db: Session, category: Categories) -> None:
    db.delete(category)
