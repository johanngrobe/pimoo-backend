from enum import Enum
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.database import Base
from app.utils.enum_util import RoleEnum


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(
        nullable=False, comment="First name of the user."
    )
    last_name: Mapped[str] = mapped_column(
        nullable=False, comment="Last name of the user."
    )
    role: Mapped[RoleEnum] = mapped_column(nullable=False, comment="Role of the user.")

    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id"),
        nullable=False,
        comment="Municipality ID by which the user is associated.",
    )
    municipality: Mapped["Municipality"] = relationship(
        back_populates="users", lazy="joined"
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()"), comment="Date of creation."
    )


from app.models.municipality import Municipality
