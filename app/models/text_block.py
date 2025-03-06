from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.association_text_block_tag import text_block_tag_association


class TextBlock(Base):
    __tablename__ = "text_block"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Text block ID",
    )
    label: Mapped[str] = mapped_column(
        nullable=False, comment="Label or name of the text block."
    )
    tags: Mapped[Optional[List["Tag"]]] = relationship(
        secondary=text_block_tag_association, cascade="all, delete", lazy="selectin"
    )
    municipality_id: Mapped[int] = mapped_column(
        ForeignKey("municipality.id"),
        nullable=False,
        comment="Municipality ID by which the text block is associated.",
    )
    municipality: Mapped["Municipality"] = relationship()
    created_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True,
        comment="User ID of the creator of the text block.",
    )
    author: Mapped[Optional["User"]] = relationship(
        foreign_keys=[created_by], lazy="selectin"
    )
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id"), nullable=True, comment="User ID of the last editor."
    )
    last_editor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[last_edited_by], lazy="selectin"
    )


# Late imports
from app.models.municipality import Municipality
from app.models.tag import Tag
from app.models.user import User
