from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MobilityResult(Base):
    __tablename__ = "mobility_result"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Mobility result ID",
    )

    submission_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mobility_submission.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Submission ID by which the mobility result is associated.",
    )
    submission: Mapped["MobilitySubmission"] = relationship(
        back_populates="objectives", lazy="selectin"
    )
    main_objective_id: Mapped[int] = mapped_column(
        ForeignKey("main_objective.id"),
        nullable=False,
        comment="Main objective ID by which the mobility result is associated",
    )
    main_objective: Mapped["MainObjective"] = relationship(lazy="selectin")
    target: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Main Objective is targeted or not"
    )
    sub_objectives: Mapped[Optional[List["MobilitySubresult"]]] = relationship(
        back_populates="main_objective", cascade="all, delete", lazy="selectin"
    )


# Late imports
from app.models.main_objective_model import MainObjective
from app.models.mobility_submission_model import MobilitySubmission
from app.models.mobility_subresult_model import MobilitySubresult
