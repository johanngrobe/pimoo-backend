from typing import List, Optional

from datetime import datetime, date
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.core.db import Base


class MobilitaetscheckEingabe(Base):
    __tablename__ = "mobilitaetscheck_eingabe"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Mobilitätscheck-Eingabe",
    )
    verwaltungsvorgang_nr: Mapped[str] = mapped_column(
        nullable=False,
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
        nullable=False, comment="Beschreibung der Mobilitätschecks"
    )
    erstellt_am: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()"), comment="Zeitpunkt der Erstellung"
    )

    eingabe_ziel_ober: Mapped[Optional[List["MobilitaetscheckEingabeZielOber"]]] = (
        relationship(
            back_populates="eingabe",
            cascade="all, delete-orphan",
            passive_deletes=True,
            lazy="selectin",
        )
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID, mit der die Mobilitätscheck-Eingabe verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des Erstellers der Mobilitätschecks",
    )
    autor: Mapped["User"] = relationship(foreign_keys=[erstellt_von], lazy="joined")
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped["User"] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von], lazy="joined"
    )
    veroeffentlicht: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Markiert, ob die Eingabe veröffentlicht ist oder nicht",
    )


# Late imports
from app.models.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOber,
)
from app.models.gemeinde import Gemeinde
from app.models.user import User
