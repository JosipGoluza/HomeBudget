from sqlalchemy.orm import Session

from app.models.user_model import User
from sqlalchemy import select


def get_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def get_by_email_or_username(db: Session, email: str, username: str) -> User | None:
    return db.scalar(select(User).where(
        (User.email == email) | (User.username == username)
    ))


def add_user(db: Session, user: User) -> User:
    db.add(user)
    db.flush()
    return user
