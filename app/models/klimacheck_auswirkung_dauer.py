from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimacheckAuswirkungDauer(Base):
    __tablename__ = "klimacheck_auswirkung_dauer"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Auswirkungsdauer für den Klimacheck",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Titel der Auswirkungsdauer"
    )
    alt_name: Mapped[str] = mapped_column(
        nullable=True, comment="Optionaler alternativer Name der Auswirkungsdauer"
    )
