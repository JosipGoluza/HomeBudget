from sqlalchemy import Table, ForeignKey, Column

from app.core.database import Base

user_categories_xref = Table(
    "user_categories_xref",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("categories_id", ForeignKey("categories.id")),
)

