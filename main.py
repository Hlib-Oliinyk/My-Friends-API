from fastapi import FastAPI
from app.db.database import Base, engine
from contextlib import asynccontextmanager
from app.db.models import *
from app.api.v1 import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, docs_url='/api/docs')


app.include_router(users_router)
app.include_router(authorization_router)
app.include_router(friend_router)
app.include_router(friend_groups_router)
app.include_router(friend_group_members)


@app.get("/")
def root():
    return {
        "message": "Welcome to My Friend API",
        "docs": "/api/docs"
    }