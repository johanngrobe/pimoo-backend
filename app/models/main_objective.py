from ..database import Base
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from fastapi_users_db_sqlalchemy.generics import GUID


class MainObjective(Base):
    __tablename__ = "main_objective"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    no: Mapped[int]
    label: Mapped[str]
    sub_objectives: Mapped[List["SubObjective"]] = relationship(back_populates="main_objective", cascade="all, delete")

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

    created_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    author: Mapped[Optional["User"]] = relationship(foreign_keys=[created_by])
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    last_editor: Mapped[Optional["User"]] = relationship(foreign_keys=[last_edited_by])

# Late imports
from .sub_objective import SubObjective
from .municipality import Municipality
from .user import User
