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
    label: Mapped[str] = mapped_column(
        nullable=False, comment="Label or name of the tag"
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id", ondelete="CASCADE"),
        nullable=False,
        comment="Municipality ID by which the tag is associated.",
    )
    municipality: Mapped["Municipality"] = relationship(lazy="selectin")

    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID of the creator of the tag.",
    )
    author: Mapped[Optional["User"]] = relationship(
        foreign_keys=[created_by], lazy="selectin"
    )
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULl"),
        nullable=True,
        comment="User ID of the last editor.",
    )
    last_editor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[last_edited_by], lazy="selectin"
    )


# Late imports
from app.models.municipality import Municipality
from app.models.user import User
