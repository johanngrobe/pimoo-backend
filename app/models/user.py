from enum import Enum
from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.core.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    vorname: Mapped[str] = mapped_column(
        nullable=False, comment="Vorname des Benutzers"
    )
    nachname: Mapped[str] = mapped_column(
        nullable=False, comment="Nachname des Benutzers"
    )
    rolle: Mapped[str] = mapped_column(nullable=False, comment="Rolle des Benutzers")

    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID, mit der der Benutzer verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(back_populates="users", lazy="selectin")
    erstellt_am: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("now()"),
        comment="Zeitpunkt der Erstellung des Benutzers",
    )


from app.models.gemeinde import Gemeinde
