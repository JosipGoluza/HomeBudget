from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr = Field(
        description="Valid email address for the account",
        examples=["test@example.com"]
    )
    username: str = Field(
        description="Unique username for the account (3-50 characters)",
        min_length=3,
        max_length=50,
        examples=["test_username"]
    )
    password: str = Field(
        description="Password for account (at least 12 characters)",
        min_length=12,
        max_length=100,
        examples=["password_min_12"]
    )


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(
        default=None,
        description="Updated email address",
        examples=["newemail@example.com"]
    )
    username: str | None = Field(
        default=None,
        description="Updated username",
        min_length=3,
        max_length=50,
        examples=["new_username"]
    )


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique user identifier")
    email: EmailStr = Field(description="User's email address")
    username: str = Field(description="User's username")


class Token(BaseModel):
    access_token: str = Field(
        description="JWT access token for authenticating API requests",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTYyNDU4NTYwMH0.signature"]
    )
    token_type: str = Field(
        description="Type of token (always 'bearer' for this API)"
    )


class TokenData(BaseModel):
    username: str | None = Field(
        description="Username extracted from JWT token"
    )
