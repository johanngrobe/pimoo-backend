from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database import Base

# association table for many-to-many relationship between indicators and tags
indicator_tag_association = Table(
    'indicator_tag',
    Base.metadata,
    Column('indicator_id', Integer, ForeignKey('indicator.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"))
)