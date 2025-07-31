from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Gemeinde(Base):
    __tablename__ = "gemeinde"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeinde ID",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name der Gemeinde oder Stadt"
    )
    users: Mapped[Optional[List["User"]]] = relationship(
        back_populates="gemeinde", cascade="all, delete", lazy="selectin"
    )
    gebiete: Mapped[Optional[List["GemeindeGebiet"]]] = relationship(
        back_populates="gemeinde", cascade="all, delete", lazy="selectin"
    )


from app.models.user import User
from app.models.gemeinde_gebiet import GemeindeGebiet
