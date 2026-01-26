from pydantic import BaseModel, Field


class FriendGroupCreate(BaseModel):
    name: str = Field(min_length=5, max_length=100)


class FriendGroupUpdate(BaseModel):
    name: str | None = None


class FriendGroupResponse(BaseModel):
    id: int
    user_id: int
    name: str

    model_config = {
        "from_attributes": True
    }
