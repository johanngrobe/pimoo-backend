from typing import Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SubObjective(Base):
    __tablename__ = "sub_objective"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Sub objective ID",
    )
    no: Mapped[int] = mapped_column(nullable=False, comment="Sub objective number")
    label: Mapped[str] = mapped_column(
        nullable=False, comment="Label or name of sub objective"
    )
    main_objective_id: Mapped[int] = mapped_column(
        ForeignKey("main_objective.id"),
        nullable=False,
        comment="Main objective ID associated with the sub objective",
    )
    main_objective: Mapped["MainObjective"] = relationship(
        back_populates="sub_objectives", cascade="all, delete", lazy="selectin"
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id"),
        nullable=False,
        comment="Municipality ID by which the sub objective is associated.",
    )
    municipality: Mapped["Municipality"] = relationship(lazy="selectin")
    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True,
        comment="User ID of the creator of the sub objective.",
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
from app.models.main_objective_model import MainObjective
from app.models.municipality_model import Municipality
from app.models.user_model import User
