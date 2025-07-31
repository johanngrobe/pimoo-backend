from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between mobility_results and indicators
magistratsvorlage_gemeindeGebiet_assoziation = Table(
    "magistratsvorlage_gemeindeGebiet",
    Base.metadata,
    Column(
        "gemeinde_gebiet_id",
        Integer,
        ForeignKey("gemeinde_gebiet.id", ondelete="CASCADE"),
    ),
    Column(
        "magistratsvorlage_id",
        Integer,
        ForeignKey("magistratsvorlage.id", ondelete="CASCADE"),
    ),
)
