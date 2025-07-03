from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between text_blocks and tags
textblock_tag_assoziation = Table(
    "textblock_tag",
    Base.metadata,
    Column("textblock_id", Integer, ForeignKey("textblock.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE")),
)
