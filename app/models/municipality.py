from ..database import Base
from typing import Optional, List
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Municipality(Base):
    __tablename__ = "municipality"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    name: Mapped[str]

    users: Mapped[Optional[List["User"]]] = relationship(back_populates="municipality")

from .user import User