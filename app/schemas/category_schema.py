from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(min_length=3, max_length=50, default=None)


class CategoryGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None