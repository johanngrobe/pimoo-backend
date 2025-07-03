from typing import List, Optional, Literal

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.core.db import Base

from app.models.assoziation_mobilitaetscheckEingabeZielUnter_indikator import (
    mobilitaetscheckEingabeZielUnter_indikator_assoziation,
)


class MobilitaetscheckEingabeZielUnter(Base):
    __tablename__ = "mobilitaetscheck_eingabe_ziel_unter"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Mobilitätscheck Eingabe Unterziels",
    )

    eingabe_ziel_ober_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_eingabe_ziel_ober.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID der Mobilitätscheck Eingabe Oberziels, mit dem das Unterziel verknüpft ist",
    )
    eingabe_ziel_ober: Mapped["MobilitaetscheckEingabeZielOber"] = relationship(
        back_populates="eingabe_ziel_unter", lazy="selectin"
    )
    ziel_unter_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_unter.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID des Mobilitätscheck Unterziels, mit dem die Eingabe verknüpft ist",
    )
    ziel_unter: Mapped["MobilitaetscheckZielUnter"] = relationship(lazy="selectin")
    tangiert: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Markiert, ob das Unterziel tangiert ist"
    )
    auswirkung: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        comment="Auswirkung des Unterziels",
    )
    auswirkung_raeumlich: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Räumliche Auswirkung des Unterziels",
    )
    anmerkung: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Anmerkung zum Unterziel"
    )
    indikatoren: Mapped[Optional[List["Indikator"]]] = relationship(
        secondary=mobilitaetscheckEingabeZielUnter_indikator_assoziation,
        passive_deletes=True,
        lazy="selectin",
    )


# Late imports
from app.models.indikator import Indikator
from app.models.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnter
from app.models.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOber,
)
