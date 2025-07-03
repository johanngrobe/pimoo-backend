from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between indicators and tags
indikator_tag_assoziation = Table(
    "indikator_tag",
    Base.metadata,
    Column("indikator_id", Integer, ForeignKey("indikator.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE")),
)
