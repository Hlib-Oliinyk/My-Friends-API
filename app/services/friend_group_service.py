from sqlalchemy import select
from fastapi import HTTPException
from app.db.models.friend_groups import FriendGroup
from app.schemas.friend_group import FriendGroupCreate, FriendGroupUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_user_friend_groups(db: AsyncSession, user_id: int):
    stmt = select(FriendGroup).filter(FriendGroup.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_friend_group(db: AsyncSession, user_id: int, friend_group_id: int):
    stmt = select(FriendGroup).filter(FriendGroup.user_id == user_id,
                                        FriendGroup.id == friend_group_id)
    result = await db.execute(stmt)
    friend_group = result.scalar_one_or_none()

    if friend_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return friend_group


async def add_friend_group(db: AsyncSession, friend_group: FriendGroupCreate, user_id: int):
    new_friend_group = FriendGroup(
        user_id = user_id,
        name = friend_group.name,
    )

    db.add(new_friend_group)
    await db.commit()
    await db.refresh(new_friend_group)
    return new_friend_group


async def update_friend_group(db: AsyncSession, friend_group_id: int, user_id: int, friend_group: FriendGroupUpdate):
    updated_group = await get_user_friend_group(db, user_id, friend_group_id)

    if not updated_group:
        return False

    if friend_group.name is not None:
        updated_group.name = friend_group.name

    await db.commit()
    await db.refresh(updated_group)
    return updated_group


async def delete_friend_group(db: AsyncSession, friend_group_id: int, user_id: int):
    friend_group = await get_user_friend_group(db, user_id, friend_group_id)

    if not friend_group:
        return False

    await db.delete(friend_group)
    await db.commit()
    return True