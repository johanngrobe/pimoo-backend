from ..database import Base
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped

class MobilitySubmission(Base):
    __tablename__ = "mobility_submission"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    author: Mapped[str]
    administration_no: Mapped[str]
    administration_date: Mapped[date]
    label: Mapped[str]
    desc: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))

    objectives: Mapped[Optional[List["MobilityResult"]]] = relationship(back_populates="submission", cascade="all, delete-orphan", passive_deletes=True)

    # municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    # municipality: Mapped["Municipality"] = relationship()

# Late imports
from .mobility_result import MobilityResult