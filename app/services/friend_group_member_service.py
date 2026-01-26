from sqlalchemy import select
from app.db.models.friend_group_members import FriendGroupMember
from app.db.models.friends import Friend
from app.db.models.friend_groups import FriendGroup
from app.schemas.friend_group_member import FriendGroupMemberCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


async def get_user_friend_group_members(db: AsyncSession, friend_group_id: int):
    stmt = (select(Friend)
            .join(FriendGroupMember)
            .where(FriendGroupMember.group_id == friend_group_id))
    result = await db.execute(stmt)
    return result.scalars().all()


async def add_friend_group_member(db: AsyncSession, data: FriendGroupMemberCreate):
    try:
        stmt = select(Friend).filter(Friend.id == data.friend_id)
        result = await db.execute(stmt)
        friend = result.scalar_one_or_none()
        if not friend:
            return None

        stmt = select(FriendGroup).filter(FriendGroup.id == data.group_id)
        result = await db.execute(stmt)
        group = result.scalar_one_or_none()
        if not group:
            return None

        stmt = select(FriendGroupMember).filter(FriendGroupMember.friend_id == data.friend_id,
                                                    FriendGroupMember.group_id == data.group_id)
        result = await db.execute(stmt)
        exists = result.scalar_one_or_none()

        if exists:
            return None

        new_group_member = FriendGroupMember(
            friend_id = data.friend_id,
            group_id = data.group_id
        )

        db.add(new_group_member)
        await db.commit()
        await db.refresh(new_group_member)
        return new_group_member

    except SQLAlchemyError:
        await db.rollback()
        raise


async def delete_friend_group_member(db: AsyncSession, group_id: int, friend_id: int):
    try:
        stmt = select(Friend).filter(Friend.id == friend_id)
        result = await db.execute(stmt)
        friend = result.scalar_one_or_none()
        if not friend:
            return None

        stmt = select(FriendGroup).filter(FriendGroup.id == group_id)
        result = await db.execute(stmt)
        group = result.scalar_one_or_none()
        if not group:
            return None

        stmt = select(FriendGroupMember).filter(FriendGroupMember.friend_id == friend_id,
                                                    FriendGroupMember.group_id == group_id)
        result = await db.execute(stmt)
        exists = result.scalar_one_or_none()

        if exists:
            await db.delete(exists)
            await db.commit()
            return True

        return False

    except SQLAlchemyError:
        await db.rollback()
        raise


