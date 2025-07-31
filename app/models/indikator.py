from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.assoziation_indikator_tag import indikator_tag_assoziation


class Indikator(Base):
    __tablename__ = "indikator"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Indikator ID",
    )
    name: Mapped[str] = mapped_column(nullable=False, comment="Name des Indikators")
    quelle_url: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="URL zur Quelle des Indikators"
    )
    tags: Mapped[Optional[List["Tag"]]] = relationship(
        secondary=indikator_tag_assoziation, lazy="selectin"
    )
    gemeindespezifisch: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Gibt an, ob der Indikator mit anderen Gemeinden geteilt wird oder gemeindespezifisch ist",
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey(
            "gemeinde.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Gemeinde ID, mit der der Indikator verknüpft ist.",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des Erstellers des Indikators",
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
from app.models.tag import Tag
from app.models.user import User
