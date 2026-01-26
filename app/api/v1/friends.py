from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_user
from app.db.database import get_db
from app.db.models.users import User
import app.services.friend_service as friend_service
from app.schemas.friend import FriendCreate, FriendUpdate, FriendResponse


router = APIRouter(prefix="/friends", tags=["Friends"])


@router.get("/", response_model=list[FriendResponse])
async def get_all_friends(pagination: friend_service.PaginationDep,
                          current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    return await friend_service.get_all_friends(db, current_user.id, pagination)


@router.get("/{friend_id}", response_model=FriendResponse)
async def get_friend(friend_id: int, current_user: User = Depends(get_current_user),
               db: AsyncSession = Depends(get_db)):
    return await friend_service.get_friend(db, friend_id, current_user.id)


@router.post("/{friend_id}")
async def add_friend(friend: FriendCreate, current_user: User = Depends(get_current_user),
               db: AsyncSession = Depends(get_db)):
    return await friend_service.add_friend(db, friend, current_user.id)


@router.put("/{friend_id}")
async def update_friend(friend_id: int, friend: FriendUpdate, current_user: User = Depends(get_current_user),
                  db: AsyncSession = Depends(get_db)):
    return await friend_service.update_friend(db, friend_id, current_user.id, friend)


@router.delete("/{friend_id}")
async def delete_friend(friend_id: int, current_user: User = Depends(get_current_user),
                  db: AsyncSession = Depends(get_db)):
    return await friend_service.delete_friend(db, friend_id, current_user.id)