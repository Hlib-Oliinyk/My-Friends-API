from sqlalchemy import select
from fastapi import HTTPException
from app.db.models.users import User
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from app.core.security import hash_password, verify_password


async def get_users(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def check_user(db: AsyncSession, email: str, username: str):
    stmt = select(User).filter(or_(User.email == email, User.username == username))
    result = await db.execute(stmt)
    return result.scalars().first()


async def add_user(db: AsyncSession, user: UserCreate):
    if await check_user(db, user.email, user.username):
        raise HTTPException(400, "User exists")

    new_user = User(
        email = user.email,
        username = user.username,
        password_hashed = hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)

    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True


async def login_user(db: AsyncSession, login: str, password: str):
    stmt = select(User).filter(or_(User.username == login,
                                     User.email == login))

    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return False

    if not verify_password(password, user.password_hashed):
        return False

    return user