from ..database import Base
from datetime import datetime, date
from typing import Optional, Literal
from sqlalchemy import ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy.generics import GUID


Impact_enum = Literal["positive", "negative", "no_effect"]
Impact_duration_enum = Literal["short", "medium", "long"]

class ClimateSubmission(Base):
    __tablename__ = "climate_submission"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    administration_no: Mapped[str]
    administration_date: Mapped[date]
    label: Mapped[str]
    impact: Mapped[Impact_enum]
    impact_ghg: Mapped[Optional[int]]
    impact_adaption: Mapped[Optional[int]]
    impact_desc: Mapped[Optional[str]]
    impact_duration: Mapped[Optional[Impact_duration_enum]]
    alternative_desc: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

    created_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    author: Mapped[Optional["User"]] = relationship(foreign_keys=[created_by])
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    last_editor: Mapped[Optional["User"]] = relationship(foreign_keys=[last_edited_by])

    is_published: Mapped[bool] = mapped_column(nullable=False, default=False)

# Late imports
from .municipality import Municipality
from .user import User