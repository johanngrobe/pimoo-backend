from ..database import Base
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .tag import Tag
from .association_tables import indicator_tag_association

class Indicator(Base):
    __tablename__ = "indicator"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]
    source: Mapped[str] = mapped_column(nullable=True)
    source_url: Mapped[str] = mapped_column(nullable=True)
    tags: Mapped[Optional[List[Tag]]] = relationship(secondary=indicator_tag_association, cascade="all, delete")


    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

# Late imports
from .municipality import Municipality