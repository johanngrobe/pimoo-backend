from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class GemeindeGebiet(Base):
    __tablename__ = "gemeinde_gebiet"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindegebiet ID",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name des Gemeindegebiets"
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID mit der das Gebiet verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(
        back_populates="gebiete", cascade="all, delete", lazy="selectin"
    )


from app.models.gemeinde import Gemeinde
