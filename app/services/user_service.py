from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import PREDEFINED_CATEGORIES
from app.models.category_model import Categories
from app.models.user_model import User
from app.repositories import user_repository
from app.schemas.user_schema import UserCreate, UserOut
from app.services.auth_service import get_password_hash


def create_user(db: Session, body: UserCreate) -> UserOut:
    if user_repository.get_by_email_or_username(db, body.email, body.username):
        raise HTTPException(status_code=400, detail="Email or username already exists")

    user = User(
        email=body.email,
        username=body.username,
        hashed_password=get_password_hash(body.password),
    )
    user_repository.add_user(db, user)

    for name, description in PREDEFINED_CATEGORIES:
        db.add(Categories(name=name, description=description, user_id=user.id))

    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)
