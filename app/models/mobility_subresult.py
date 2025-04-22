from typing import List, Optional, Literal

from enum import Enum
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.core.db import Base

from .association_results_indicators import (
    mobility_results_indicators_association,
)


class SpatialImpactEnum(str, Enum):
    locally = "locally"
    districtwide = "districtwide"
    citywide = "citywide"


class MobilitySubresult(Base):
    __tablename__ = "mobility_subresult"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Mobility Subresult ID",
    )

    mobility_result_id: Mapped[int] = mapped_column(
        ForeignKey("mobility_result.id", ondelete="CASCADE"),
        nullable=False,
        comment="Associated Mobility Result ID",
    )
    main_objective: Mapped["MobilityResult"] = relationship(
        back_populates="sub_objectives", lazy="selectin"
    )
    sub_objective_id: Mapped[int] = mapped_column(
        ForeignKey("sub_objective.id", ondelete="CASCADE"),
        nullable=False,
        comment="Sub Objective ID by which the mobility subresult is associated",
    )
    sub_objective: Mapped["SubObjective"] = relationship(lazy="selectin")
    target: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Sub Objective is targeted or not"
    )
    impact: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        comment="Impact on the sub objective on a scale from -3 to 3",
    )
    spatial_impact: Mapped[Optional[SpatialImpactEnum]] = mapped_column(
        nullable=True,
        comment="Spatial impact of the sub objective (e.g. locally, districtwide, citywide)",
    )
    annotation: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Annotation for the sub objective"
    )
    indicators: Mapped[Optional[List["Indicator"]]] = relationship(
        secondary=mobility_results_indicators_association,
        passive_deletes=True,
        lazy="selectin",
    )


# Late imports
from app.models.indicator import Indicator
from app.models.main_objective import SubObjective
from app.models.mobility_result import MobilityResult
