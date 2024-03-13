from sqlalchemy.orm import Mapped, mapped_column
from DB.database import Base, str_256
from sqlalchemy import text, ForeignKey, Boolean
import datetime
from typing import Annotated
from enum import Enum

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


class StatusTask(Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    user_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_256] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")
    is_block: Mapped[bool] = mapped_column(Boolean, server_default="false")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class UserAuthOrm(Base):
    __tablename__ = "auth"

    user_id: Mapped[intpk] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    email: Mapped[str_256] = mapped_column(nullable=False)
    password: Mapped[str_256] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class TaskOrm(Base):
    __tablename__ = "task"

    id: Mapped[intpk]
    title: Mapped[str_256] = mapped_column(nullable=False)
    description: Mapped[str_256] = mapped_column(nullable=False)
    deadline: Mapped[datetime.date] = mapped_column(nullable=False)
    performer_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    status: Mapped[StatusTask] = mapped_column(default=StatusTask.CREATED)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
