from ..database import Base
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .main_objective import MainObjective

class MobilityResult(Base):
    __tablename__ = "mobility_result"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)

    submission_id: Mapped[int] = mapped_column(ForeignKey("mobility_submission.id", ondelete="CASCADE"))
    submission: Mapped["MobilitySubmission"] = relationship(back_populates="objectives")

    main_objective_id: Mapped[int] = mapped_column(ForeignKey("main_objective.id"))
    main_objective: Mapped[MainObjective] = relationship()
    target: Mapped[bool] = mapped_column(nullable=False, default=False)

    sub_objectives: Mapped[Optional[List["MobilitySubresult"]]] = relationship(back_populates="main_objective", cascade="all, delete")

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

# Late imports
from .mobility_submission import MobilitySubmission
from .mobility_subresult import MobilitySubresult
from .municipality import Municipality