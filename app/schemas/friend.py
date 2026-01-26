from datetime import date
from pydantic import BaseModel, Field, EmailStr


class FriendCreate(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    phone: str | None = None
    email: EmailStr | None = None
    birthdate: date | None = None


class FriendUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    birthdate: date | None = None


class FriendResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    birthdate: date

    model_config = {
        "from_attributes": True
    }


class FriendPagination(BaseModel):
    limit: int= Field(5, ge=0, le=100)
    offset: int = Field(0, ge=0)