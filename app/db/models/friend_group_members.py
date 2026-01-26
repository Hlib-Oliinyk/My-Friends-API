from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FriendGroupMember(Base):
    __tablename__ = "friend_group_members"

    id: Mapped[int] = mapped_column(primary_key = True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("friends.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("friend_groups.id"))

    friends: Mapped[list["Friend"]] = relationship(back_populates="friend_group_members")
    friend_groups: Mapped[list["FriendGroup"]] = relationship(back_populates="friend_group_members")