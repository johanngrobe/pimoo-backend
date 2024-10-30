from ..database import Base
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from fastapi_users_db_sqlalchemy.generics import GUID

class SubObjective(Base):
    __tablename__ = "sub_objective"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    no: Mapped[int]
    label: Mapped[str]
    main_objective_id: Mapped[int] = mapped_column(ForeignKey("main_objective.id"), nullable=False)
    main_objective: Mapped["MainObjective"] = relationship(back_populates="sub_objectives",cascade="all, delete")

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

    created_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    author: Mapped[Optional["User"]] = relationship(foreign_keys=[created_by])
    last_edited_by: Mapped[Optional[GUID]] = mapped_column(ForeignKey("user.id"))
    last_editor: Mapped[Optional["User"]] = relationship(foreign_keys=[last_edited_by])

# Late imports
from .main_objective import MainObjective
from .municipality import Municipality
from .user import User
