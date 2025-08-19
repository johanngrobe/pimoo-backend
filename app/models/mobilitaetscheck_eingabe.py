from typing import List, Optional

from datetime import datetime, date
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.core.db import Base
from app.models.assoziation_mobilitaetscheckEingabe_user import (
    mobilitaetscheckEingabe_user_assoziation,
)


class MobilitaetscheckEingabe(Base):
    __tablename__ = "mobilitaetscheck_eingabe"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID der Mobilitätscheck-Eingabe",
    )
    name: Mapped[str] = mapped_column(
        nullable=True, comment="Name der Mobilitätscheck-Eingabe"
    )
    erstellt_am: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()"), comment="Zeitpunkt der Erstellung"
    )
    magistratsvorlage_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("magistratsvorlage.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID der zugehörigen Magistratsvorlage",
    )
    magistratsvorlage: Mapped[Optional["Magistratsvorlage"]] = relationship(
        back_populates="mobilitaetschecks",
        lazy="selectin",
    )

    eingabe_ziel_ober: Mapped[Optional[List["MobilitaetscheckEingabeZielOber"]]] = (
        relationship(
            back_populates="eingabe",
            order_by=lambda: MobilitaetscheckEingabeZielOber.ziel_ober_nr,
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
    user: Mapped[Optional[List["User"]]] = relationship(
        secondary=mobilitaetscheckEingabe_user_assoziation,
        passive_deletes=True,
        lazy="selectin",
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
from app.models.magistratsvorlage import Magistratsvorlage
from app.models.user import User
