from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Municipality(Base):
    __tablename__ = "municipality"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Municipality ID",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name of the municipality."
    )
    users: Mapped[Optional[List["User"]]] = relationship(
        back_populates="municipality", cascade="all, delete", lazy="selectin"
    )


from app.models.user import User
