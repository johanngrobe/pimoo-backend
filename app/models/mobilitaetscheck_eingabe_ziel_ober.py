from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckEingabeZielOber(Base):
    __tablename__ = "mobilitaetscheck_eingabe_ziel_ober"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Eingabe des Mobilitätschecks für das Oberziel",
    )

    mobilitaetscheck_eingabe_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mobilitaetscheck_eingabe.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Eingabe ID des Mobilitätschecks, mit der das Oberziel verknüpft ist",
    )
    mobilitaetscheck_eingabe: Mapped["MobilitaetscheckEingabe"] = relationship(
        back_populates="objectives", lazy="selectin"
    )
    mobilitaetscheck_ziel_ober_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_ober.id"),
        nullable=False,
        comment="ID des Leitziels, mit dem die Eingabe verknüpft ist",
    )
    mobilitaetscheck_ziel_ober: Mapped["MobilitaetscheckZielOber"] = relationship(
        lazy="selectin"
    )
    tangiert: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Markiert, ob das Oberziel tangiert ist"
    )
    mobilitaetscheck_eingabe_ziel_unter: Mapped[
        Optional[List["MobilitaetscheckEingabeZielUnter"]]
    ] = relationship(
        back_populates="mobilitaetscheck_eingabe_ziel_ober",
        cascade="all, delete",
        lazy="selectin",
    )


# Late imports
from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnter,
)
