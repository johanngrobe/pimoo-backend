from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.assoziation_textblock_tag import textblock_tag_assoziation


class Textblock(Base):
    __tablename__ = "textblock"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Textblock ID",
    )
    name: Mapped[str] = mapped_column(nullable=False, comment="Name des Textblocks")
    tags: Mapped[Optional[List["Tag"]]] = relationship(
        secondary=textblock_tag_assoziation, cascade="all, delete", lazy="selectin"
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID, mit der der Textblock verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des Erstellers des Textblocks",
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
from app.models.gemeinde import Gemeinde
from app.models.tag import Tag
from app.models.user import User
