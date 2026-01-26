from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.friend_group_member import FriendGroupMemberCreate, FriendGroupMemberResponse
import app.services.friend_group_member_service as friend_group_member_service


router = APIRouter(prefix="/friend_group_members", tags=["Friend Group Members"])


@router.get("/{friend_group_id}", response_model=list[FriendGroupMemberResponse])
async def get_user_friend_group_members(friend_group_id: int, db: AsyncSession = Depends(get_db)):
    return await friend_group_member_service.get_user_friend_group_members(db, friend_group_id)


@router.post("/")
async def add_friend_group_member(data: FriendGroupMemberCreate, db: AsyncSession = Depends(get_db)):
    return await friend_group_member_service.add_friend_group_member(db, data)


@router.delete("/{friend_group_id}")
async def delete_friend_group_member(friend_id: int, group_id: int, db: AsyncSession = Depends(get_db)):
    return await friend_group_member_service.delete_friend_group_member(db, group_id, friend_id)