from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimacheckKlimarelevanz(Base):
    __tablename__ = "klimacheck_klimarelevanz"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Klimarelevanz für den Klimacheck",
    )
    name: Mapped[str] = mapped_column(nullable=False, comment="Name der Klimarelevanz")
