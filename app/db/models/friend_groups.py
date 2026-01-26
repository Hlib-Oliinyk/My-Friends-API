from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FriendGroup(Base):
    __tablename__ = "friend_groups"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="friend_groups")
    friend_group_members: Mapped["FriendGroupMember"] = relationship(back_populates="friend_groups")