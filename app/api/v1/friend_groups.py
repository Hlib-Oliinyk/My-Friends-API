from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_user
from app.db.database import get_db
from app.db.models.users import User
from app.schemas.friend_group import FriendGroupCreate, FriendGroupResponse, FriendGroupUpdate
import app.services.friend_group_service as friend_group_service


router = APIRouter(prefix="/friend_groups", tags=["Friend Groups"])


@router.get("/", response_model=list[FriendGroupResponse])
async def get_all_user_friend_groups(current_user: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    return await friend_group_service.get_all_user_friend_groups(db, current_user.id)


@router.get("/{friend_group_id}", response_model=FriendGroupResponse)
async def get_user_friend_group(friend_group_id: int, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    return await friend_group_service.get_user_friend_group(db, current_user.id, friend_group_id)


@router.post("/{friend_group_id}")
async def add_friend_group(friend_group: FriendGroupCreate, current_user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    return await friend_group_service.add_friend_group(db, friend_group, current_user.id)


@router.put("/{friend_group_id}")
async def update_friend_group(friend_group_id: int, data: FriendGroupUpdate,
                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await friend_group_service.update_friend_group(db, friend_group_id, current_user.id, data)


@router.delete("/{friend_group_id}")
async def delete_friend_group(friend_group_id: int, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    return await friend_group_service.delete_friend_group(db, friend_group_id, current_user.id)
