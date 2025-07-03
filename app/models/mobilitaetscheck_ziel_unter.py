from typing import Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckZielUnter(Base):
    __tablename__ = "mobilitaetscheck_ziel_unter"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID des Unterziels für den Mobilitätscheck",
    )
    nr: Mapped[int] = mapped_column(
        nullable=False, comment="Nummerierung des Unterziels"
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name oder Bezeichnung des Unterziels"
    )
    ziel_ober_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_ober.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID des Oberziels, mit dem das Unterziel verknüpft ist",
    )
    ziel_ober: Mapped["MobilitaetscheckZielOber"] = relationship(
        back_populates="ziel_unter", lazy="selectin"
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID, mit der das Unterziel verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des Erstellers des Unterziels",
    )
    autor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[erstellt_von], lazy="selectin"
    )
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von], lazy="selectin"
    )


# Late imports
from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber
from app.models.gemeinde import Gemeinde
from app.models.user import User
