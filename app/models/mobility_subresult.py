from ..database import Base
from typing import List, Optional, Literal
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .main_objective import SubObjective
from .indicator import Indicator
from .association_tables import mobility_results_indicators_association

Spatial_impact_enum = Literal["locally", "districtwide", "citywide"]

class MobilitySubresult(Base):
    __tablename__ = "mobility_subresult"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)

    mobility_result_id: Mapped[int] = mapped_column(ForeignKey("mobility_result.id",ondelete="CASCADE"))
    main_objective: Mapped["MobilityResult"] = relationship(back_populates="sub_objectives")

    sub_objective_id: Mapped[int] = mapped_column(ForeignKey("sub_objective.id"))
    sub_objective: Mapped[SubObjective] = relationship()

    target: Mapped[bool] = mapped_column(nullable=False, default=False)
    impact: Mapped[Optional[int]]
    spatial_impact: Mapped[Optional[Spatial_impact_enum]]
    annotation: Mapped[Optional[str]]
    indicators: Mapped[Optional[List[Indicator]]] = relationship(secondary=mobility_results_indicators_association, cascade="all, delete", passive_deletes=True)

# Late imports
from .mobility_result import MobilityResult



