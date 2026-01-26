from fastapi import HTTPException, Response
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import ALGORITHM, SECRET_KEY
import app.services.user_service as user_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.add_user(db, user)


@router.post("/login")
async def login(response: Response, user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await user_service.login_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    token = jwt.encode(
        {
            "sub": str(db_user.id),
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return True
