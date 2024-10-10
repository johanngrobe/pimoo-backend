from ..database import Base
from typing import List, Optional
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .tag import Tag
from .association_tables import indicator_tag_association

class Indicator(Base):
    __tablename__ = "indicator"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]
    tags: Mapped[Optional[List[Tag]]] = relationship(secondary=indicator_tag_association, cascade="all, delete")