from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(
        description="Category name (e.g., 'Groceries', 'Utilities', 'Entertainment')",
        min_length=3,
        max_length=50,
        examples=["Groceries"]
    )
    description: str | None = Field(
        default=None,
        description="Optional description of the category",
        min_length=3,
        max_length=50,
        examples=["Household food and grocery items"]
    )


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        description="Updated category name",
        min_length=3,
        max_length=50,
        examples=["Utilities"]
    )
    description: str | None = Field(
        default=None,
        description="Updated category description",
        min_length=3,
        max_length=50,
        examples=["Monthly utility bills"]
    )


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique category identifier")
    name: str = Field(description="Category name")
    description: str | None = Field(description="Category description")
