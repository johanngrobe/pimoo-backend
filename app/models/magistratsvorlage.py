from typing import List, Optional

from datetime import datetime, date
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.core.db import Base
from app.models.assoziation_magistratsvorlage_gemeindeGebiet import (
    magistratsvorlage_gemeindeGebiet_assoziation,
)


class Magistratsvorlage(Base):
    __tablename__ = "magistratsvorlage"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Magistratsvorlage",
    )
    verwaltungsvorgang_nr: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        comment="Verwaltungsvorgangsnummer",
    )
    verwaltungsvorgang_datum: Mapped[date] = mapped_column(
        nullable=False,
        comment="Datum des Verwaltungsvorgangs",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name oder Titel der Mobilitätschecks"
    )
    beschreibung: Mapped[str] = mapped_column(
        nullable=True, comment="Beschreibung der Mobilitätschecks"
    )
    gemeinde_gebiete: Mapped[Optional[List["GemeindeGebiet"]]] = relationship(
        secondary=magistratsvorlage_gemeindeGebiet_assoziation,
        lazy="selectin",
    )
    erstellt_am: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()"), comment="Zeitpunkt der Erstellung"
    )
    veroeffentlicht: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Gibt an, ob die Magistratsvorlage veröffentlicht wurde",
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID, mit der die Mobilitätscheck-Eingabe verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")

    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID vom Ersteller des Klimachecks",
    )
    autor: Mapped[Optional["User"]] = relationship(foreign_keys=[erstellt_von])
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von]
    )
    mobilitaetschecks: Mapped[Optional[List["MobilitaetscheckEingabe"]]] = relationship(
        back_populates="magistratsvorlage",
        lazy="selectin",
    )
    klimachecks: Mapped[Optional[List["KlimacheckEingabe"]]] = relationship(
        back_populates="magistratsvorlage",
        lazy="selectin",
    )


from app.models.gemeinde import Gemeinde
from app.models.gemeinde_gebiet import GemeindeGebiet
from app.models.klimacheck_eingabe import KlimacheckEingabe
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.user import User
