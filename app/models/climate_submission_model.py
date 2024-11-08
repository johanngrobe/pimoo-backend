from typing import Optional

from datetime import datetime, date
from enum import Enum
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.database import Base
from app.utils.enum_util import ImpactEnum, ImpactDurationEnum


class ClimateSubmission(Base):
    """
    Represents a submission related to climate initiatives or projects.

    This model stores detailed information about the climate impact,
    adaptations, and alternatives of a specific project submitted by a
    municipality or an organization.
    """

    __tablename__ = "climate_submission"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Submission ID",
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
    impact: Mapped[ImpactEnum] = mapped_column(
        nullable=False,
        comment="Estimated impact on climate (e.g., positive, negative, no effect).",
    )
    impact_ghg: Mapped[Optional[int]] = mapped_column(
        CheckConstraint("impact_ghg BETWEEN -3 AND 3"),
        nullable=True,
        comment="Estimated impact on greenhouse gas emissions on a scale from -3 to 3.",
    )
    impact_adaption: Mapped[Optional[int]] = mapped_column(
        CheckConstraint("impact_adaption BETWEEN -3 AND 3"),
        nullable=True,
        comment="Estimated impact on climate adaptation on a scale from -3 to 3.",
    )
    impact_desc: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Detailed description of the estimated impact on climate.",
    )
    impact_duration: Mapped[Optional[ImpactDurationEnum]] = mapped_column(
        nullable=True,
        comment="Estimated duration of the impact (e.g., short, medium, long).",
    )
    alternative_desc: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Description of alternative solutions or adaptations.",
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("now()"),
        comment="Date and time the submission was created.",
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id"),
        nullable=False,
        comment="ID of the municipality that submitted the project.",
    )
    municipality: Mapped["Municipality"] = relationship(lazy="selectin")
    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True,
        comment="ID of the user who created the submission.",
    )
    author: Mapped[Optional["User"]] = relationship(foreign_keys=[created_by])
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True,
        comment="ID of the user who last edited the submission.",
    )
    last_editor: Mapped[Optional["User"]] = relationship(foreign_keys=[last_edited_by])
    is_published: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Flag indicating whether the submission is published.",
    )


# Late imports
from app.models.municipality_model import Municipality
from app.models.user_model import User
