from ..database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table

# association table for many-to-many relationship between text_blocks and tags
text_block_tag_association = Table(
    'text_block_tag',
    Base.metadata,
    Column('text_block_id', Integer, ForeignKey('text_block.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"))
)


# association table for many-to-many relationship between indicators and tags
indicator_tag_association = Table(
    'indicator_tag',
    Base.metadata,
    Column('indicator_id', Integer, ForeignKey('indicator.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"))
)

# association table for many-to-many relationship between mobility_results and indicators
mobility_results_indicators_association = Table(
    'mobility_result_indicators',
    Base.metadata,
    Column('indicator_id', Integer, ForeignKey('indicator.id', ondelete="CASCADE")),
    Column('mobility_subresult_id', Integer, ForeignKey('mobility_subresult.id', ondelete="CASCADE"))
)