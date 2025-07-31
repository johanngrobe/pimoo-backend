from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckAuswirkungRaeumlich(Base):
    __tablename__ = "mobilitaetscheck_auswirkung_raeumlich"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der räumlichen Auswirkung für den Mobilitätscheck",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Titel der räumlichen Auswirkung"
    )
