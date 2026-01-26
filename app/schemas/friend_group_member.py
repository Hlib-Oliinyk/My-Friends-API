from pydantic import BaseModel


class FriendGroupMemberCreate(BaseModel):
    friend_id: int
    group_id: int


class FriendGroupMemberResponse(BaseModel):
    name: str

    model_config = {
        "from_attributes": True
    }