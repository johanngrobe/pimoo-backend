from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database import Base

# association table for many-to-many relationship between text_blocks and tags
text_block_tag_association = Table(
    'text_block_tag',
    Base.metadata,
    Column('text_block_id', Integer, ForeignKey('text_block.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"))
)