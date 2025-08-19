from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy.sql import select
from sqlalchemy.ext.hybrid import hybrid_property


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

    eingabe_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mobilitaetscheck_eingabe.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Eingabe ID des Mobilitätschecks, mit der das Oberziel verknüpft ist",
    )
    eingabe: Mapped["MobilitaetscheckEingabe"] = relationship(
        back_populates="eingabe_ziel_ober", lazy="selectin"
    )
    ziel_ober_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_ober.id"),
        nullable=False,
        comment="ID des Leitziels, mit dem die Eingabe verknüpft ist",
    )
    ziel_ober: Mapped["MobilitaetscheckZielOber"] = relationship(lazy="selectin")

    @hybrid_property
    def ziel_ober_nr(self):
        return self.ziel_ober.nr if self.ziel_ober else None

    @ziel_ober_nr.expression
    def ziel_ober_nr(cls):
        # local import avoids early reference / circular import
        from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber

        return (
            select(MobilitaetscheckZielOber.nr)
            .where(MobilitaetscheckZielOber.id == cls.ziel_ober_id)
            .correlate(cls)
            .scalar_subquery()
        )

    tangiert: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Markiert, ob das Oberziel tangiert ist"
    )
    eingabe_ziel_unter: Mapped[Optional[List["MobilitaetscheckEingabeZielUnter"]]] = (
        relationship(
            back_populates="eingabe_ziel_ober",
            order_by=lambda: MobilitaetscheckEingabeZielUnter.ziel_unter_nr,
            cascade="all, delete",
            lazy="selectin",
        )
    )


# Late imports
from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnter,
)
