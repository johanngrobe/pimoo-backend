from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.association_indicator_tag import indicator_tag_association


class Indicator(Base):
    __tablename__ = "indicator"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Indicator ID",
    )
    label: Mapped[str] = mapped_column(
        nullable=False, comment="Label or name of the indicator."
    )
    source_url: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="URL to the source of the indicator."
    )
    tags: Mapped[Optional[List["Tag"]]] = relationship(
        secondary=indicator_tag_association, lazy="selectin"
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey(
            "municipality.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Municipality ID by which the indicator is associated.",
    )
    municipality: Mapped["Municipality"] = relationship(lazy="selectin")
    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID of the creator of the indicator.",
    )
    author: Mapped[Optional["User"]] = relationship(
        foreign_keys=[created_by], lazy="selectin"
    )
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID of the last editor.",
    )
    last_editor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[last_edited_by], lazy="selectin"
    )


# Late imports
from app.models.municipality import Municipality
from app.models.tag import Tag
from app.models.user import User
