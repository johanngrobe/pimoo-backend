from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between mobility_results and indicators
mobility_results_indicators_association = Table(
    "mobility_result_indicators",
    Base.metadata,
    Column("indicator_id", Integer, ForeignKey("indicator.id", ondelete="CASCADE")),
    Column(
        "mobility_subresult_id",
        Integer,
        ForeignKey("mobility_subresult.id", ondelete="CASCADE"),
    ),
)
