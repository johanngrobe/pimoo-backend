from typing import Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, nullable=False, unique=True, comment="Tag ID"
    )
    name: Mapped[str] = mapped_column(nullable=False, comment="Name des Tags")
    gemeindespezifisch: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Gibt an, ob der Tag mit anderen Gemeinden geteilt wird oder gemeindespezifisch ist",
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID mit der der Tag verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")

    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des Erstellers des Tags",
    )
    autor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[erstellt_von], lazy="selectin"
    )
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULl"),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von], lazy="selectin"
    )


# Late imports
from app.models.gemeinde import Gemeinde
from app.models.user import User
