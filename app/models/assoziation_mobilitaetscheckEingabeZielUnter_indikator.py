from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between mobility_results and indicators
mobilitaetscheckEingabeZielUnter_indikator_assoziation = Table(
    "mobilitaetscheckEingabeZielUnter_indikator",
    Base.metadata,
    Column("indikator_id", Integer, ForeignKey("indikator.id", ondelete="CASCADE")),
    Column(
        "mobilitaetscheck_eingabe_ziel_unter_id",
        Integer,
        ForeignKey("mobilitaetscheck_eingabe_ziel_unter.id", ondelete="CASCADE"),
    ),
)
