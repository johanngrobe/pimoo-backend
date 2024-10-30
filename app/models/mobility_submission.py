from ..database import Base
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from fastapi_users_db_sqlalchemy.generics import GUID

class MobilitySubmission(Base):
    __tablename__ = "mobility_submission"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    administration_no: Mapped[str]
    administration_date: Mapped[date]
    label: Mapped[str]
    desc: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))

    objectives: Mapped[Optional[List["MobilityResult"]]] = relationship(back_populates="submission", cascade="all, delete-orphan", passive_deletes=True)

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

    created_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(foreign_keys=[created_by])
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    last_editor: Mapped["User"] = relationship(foreign_keys=[last_edited_by])

    is_published: Mapped[bool] = mapped_column(nullable=False, default=False)

# Late imports
from .mobility_result import MobilityResult
from .municipality import Municipality
from .user import User