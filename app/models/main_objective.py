from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MainObjective(Base):
    __tablename__ = "main_objective"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Main objective ID",
    )
    no: Mapped[int] = mapped_column(nullable=False, comment="Main objective number")
    label: Mapped[str] = mapped_column(
        nullable=False, comment="Lable or name of Main objective"
    )
    sub_objectives: Mapped[List["SubObjective"]] = relationship(
        back_populates="main_objective", cascade="all, delete", lazy="selectin"
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id"),
        nullable=False,
        comment="Municipality ID by which the main objective is associated.",
    )
    municipality: Mapped["Municipality"] = relationship(lazy="selectin")
    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True,
        comment="User ID of the creator of the main objective.",
    )
    author: Mapped[Optional["User"]] = relationship(
        foreign_keys=[created_by], lazy="selectin"
    )
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"), nullable=True, comment="User ID of the last editor."
    )
    last_editor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[last_edited_by], lazy="selectin"
    )


# Late imports
from app.models.municipality import Municipality
from app.models.sub_objective import SubObjective
from app.models.user import User
