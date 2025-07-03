from typing import Optional

from datetime import datetime, date
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.core.db import Base


class KlimacheckEingabe(Base):
    """
    Represents a submission related to climate initiatives or projects.

    This model stores detailed information about the climate impact,
    adaptations, and alternatives of a specific project submitted by a
    municipality or an organization.
    """

    __tablename__ = "klimacheck_eingabe"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Klimacheck ID",
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
        nullable=False, comment="Name oder Titel des Klimachecks"
    )
    klimarelevanz: Mapped[str] = mapped_column(
        nullable=False,
        comment="Einschätzung der Klimarelevanz des Projekts (z.B. hoch, mittel, niedrig).",
    )
    auswirkung_thg: Mapped[Optional[int]] = mapped_column(
        CheckConstraint("impact_ghg BETWEEN -3 AND 3"),
        nullable=True,
        comment="Art und Umfang der Auswirkungen der THG-Emissionen",
    )
    auswirkung_klimaanpassung: Mapped[Optional[int]] = mapped_column(
        CheckConstraint("impact_adaption BETWEEN -3 AND 3"),
        nullable=True,
        comment="Art und Umfang der Auswirkungen der Klimaanpassung",
    )
    auswirkung_beschreibung: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Kurzbeschreibung der Auswirkungen",
    )
    auswirkung_dauer: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Kurzbeschreibung der Dauer der Auswirkungen",
    )
    alternativen: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Description of alternative solutions or adaptations."
    )
    erstellt_am: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("now()"),
        comment="Zeitpunkt der Erstellung des Klimachecks",
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey(
            "gemeinde.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="ID der Gemeinde, mit der der Klimacheck verknüpft ist.",
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
    zuletzt_bearbeiter_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeiter_von]
    )
    veroeffentlicht: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="f",
        comment="Markiert, ob der Klimacheck veröffentlicht ist oder nicht",
    )


# Late imports
from app.models.gemeinde import Gemeinde
from app.models.user import User
