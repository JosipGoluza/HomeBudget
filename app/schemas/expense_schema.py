from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(
        description="Amount spent (must be greater than 0)",
        gt=0,
        decimal_places=2,
        examples=[49.99]
    )
    description: str | None = Field(
        default=None,
        description="Optional description of the expense",
        max_length=255,
        examples=["Weekly grocery shopping"]
    )
    date: datetime | None = Field(
        default=None,
        description="Date and time of the expense (defaults to now if not provided)",
        examples=["2026-06-20T14:30:00"]
    )
    category_id: int = Field(
        description="ID of the category this expense belongs to",
        examples=[1]
    )


class ExpenseUpdate(BaseModel):
    amount: Decimal | None = Field(
        default=None,
        description="Updated amount spent (must be greater than 0)",
        gt=0,
        decimal_places=2,
        examples=[59.99]
    )
    description: str | None = Field(
        default=None,
        description="Updated description",
        min_length=3,
        max_length=255,
        examples=["Updated grocery shopping"]
    )
    date: datetime | None = Field(
        default=None,
        description="Updated date and time of the expense",
        examples=["2026-06-21T10:00:00"]
    )
    category_id: int | None = Field(
        default=None,
        description="Updated category ID",
        examples=[2]
    )


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique expense identifier")
    amount: Decimal = Field(description="Amount spent")
    description: str | None = Field(description="Expense description")
    date: datetime = Field(description="Date and time of the expense")
    category_id: int = Field(description="Category this expense belongs to")


class ExpenseSummaryResponse(BaseModel):
    total: Decimal = Field(description="Sum of all matched expenses")
    count: int = Field(description="Number of matched expenses")
    period_from: datetime = Field(description="Start of the resolved period (inclusive)")
    period_to: datetime = Field(description="End of the resolved period (inclusive)")
    category_id: int | None = Field(default=None, description="Category filter applied, if any")
