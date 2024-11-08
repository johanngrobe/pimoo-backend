from typing import List, Optional

from datetime import datetime, date
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.database import Base


class MobilitySubmission(Base):
    __tablename__ = "mobility_submission"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Mobility Submission ID",
    )
    administration_no: Mapped[str] = mapped_column(
        nullable=False,
        comment="Internal tracking number assigned by the administration.",
    )
    administration_date: Mapped[date] = mapped_column(
        nullable=False,
        comment="Date the submission was registered by the administration.",
    )
    label: Mapped[str] = mapped_column(
        nullable=False, comment="Short descriptive title or label for the submission."
    )
    desc: Mapped[str] = mapped_column(
        nullable=False, comment="Description of the submission."
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()"), comment="Date of creation."
    )

    objectives: Mapped[Optional[List["MobilityResult"]]] = relationship(
        back_populates="submission",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id"),
        nullable=False,
        comment="Municipality ID by which the mobility submission is associated.",
    )
    municipality: Mapped["Municipality"] = relationship(lazy="selectin")
    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True,
        comment="User ID of the creator of the mobility submission.",
    )
    author: Mapped["User"] = relationship(foreign_keys=[created_by], lazy="joined")
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"), nullable=True, comment="User ID of the last editor."
    )
    last_editor: Mapped["User"] = relationship(
        foreign_keys=[last_edited_by], lazy="joined"
    )
    is_published: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Is the submission published or not"
    )


# Late imports
from app.models.mobility_result_model import MobilityResult
from app.models.municipality_model import Municipality
from app.models.user_model import User
