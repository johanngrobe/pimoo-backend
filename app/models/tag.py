from ..database import Base
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy.generics import GUID

class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

    created_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    author: Mapped[Optional["User"]] = relationship(foreign_keys=[created_by])
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    last_editor: Mapped[Optional["User"]] = relationship(foreign_keys=[last_edited_by])

# Late imports
from .municipality import Municipality
from .user import User