from ..database import Base
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .tag import Tag
from .municipality import Municipality
from .association_tables import text_block_tag_association

class TextBlock(Base):
    __tablename__ = "text_block"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]
    tags: Mapped[Optional[List[Tag]]] = relationship(secondary=text_block_tag_association, cascade="all, delete")

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"] = relationship()

# Late imports
