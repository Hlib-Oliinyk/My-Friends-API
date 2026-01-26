from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hashed: Mapped[str] = mapped_column(nullable=False)

    friends: Mapped[list["Friend"]] = relationship(back_populates="user")
    friend_groups: Mapped[list["FriendGroup"]] = relationship(back_populates="user")
