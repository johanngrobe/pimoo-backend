from ..database import Base
from typing import List
from sqlalchemy.orm import relationship, mapped_column, Mapped


class MainObjective(Base):
    __tablename__ = "main_objective"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    no: Mapped[int]
    label: Mapped[str]
    sub_objectives: Mapped[List["SubObjective"]] = relationship(back_populates="main_objective", cascade="all, delete")

    # municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    # municipality: Mapped["Municipality"] = relationship()

# Late imports
from .sub_objective import SubObjective
