from sqlalchemy import select
from typing import Annotated
from fastapi import HTTPException, Depends
from app.db.models.friends import Friend
from app.schemas.friend import FriendCreate, FriendUpdate, FriendPagination
from sqlalchemy.ext.asyncio import AsyncSession


PaginationDep = Annotated[FriendPagination, Depends(FriendPagination)]

async def get_all_friends(db: AsyncSession, user_id: int, pagination: PaginationDep):
    stmt = (select(Friend).filter(Friend.user_id == user_id)
            .limit(pagination.limit)
            .offset(pagination.offset))

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_friend(db: AsyncSession, friend_id: int, user_id: int):
    stmt = select(Friend).filter(Friend.id == friend_id,Friend.user_id == user_id)
    result = await db.execute(stmt)
    friend = result.scalar_one_or_none()

    if friend is None:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend


async def add_friend(db: AsyncSession, friend: FriendCreate, user_id: int):
    new_friend = Friend(
        user_id = user_id,
        name = friend.name,
        phone = friend.phone,
        email = friend.email,
        birthdate = friend.birthdate
    )

    db.add(new_friend)
    await db.commit()
    await db.refresh(new_friend)
    return new_friend


async def update_friend(db: AsyncSession, friend_id: int, user_id: int, friend: FriendUpdate):
    updated_friend = await get_friend(db, friend_id, user_id)

    if not updated_friend:
        return False

    if friend.name is not None:
        updated_friend.name = friend.name
    if friend.phone is not None:
        updated_friend.phone = friend.phone
    if friend.email is not None:
        updated_friend.email = friend.email
    if friend.birthdate is not None:
        updated_friend.birthdate = friend.birthdate

    await db.commit()
    await db.refresh(updated_friend)
    return updated_friend


async def delete_friend(db: AsyncSession, friend_id: int, user_id: int):
    friend = await get_friend(db, friend_id, user_id)

    if not friend:
        return False

    await db.delete(friend)
    await db.commit()
    return True


