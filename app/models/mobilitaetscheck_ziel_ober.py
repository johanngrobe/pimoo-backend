from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckZielOber(Base):
    __tablename__ = "mobilitaetscheck_ziel_ober"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID des Oberziels für den Mobilitätscheck",
    )
    nr: Mapped[int] = mapped_column(
        nullable=False, comment="Nummerierung des Oberziels"
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name oder Bezeichnung des Oberziels"
    )
    ziel_unter: Mapped[List["MobilitaetscheckZielUnter"]] = relationship(
        back_populates="ziel_ober",
        cascade="all, delete",
        lazy="selectin",
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey(
            "gemeinde.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Gemeinde ID mit der das Oberziel verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des Erstellers des Oberziels",
    )
    autor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[erstellt_von], lazy="selectin"
    )
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von], lazy="selectin"
    )


# Late imports
from app.models.gemeinde import Gemeinde
from app.models.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnter
from app.models.user import User
