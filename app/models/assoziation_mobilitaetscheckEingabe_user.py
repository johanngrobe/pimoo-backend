from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between mobility_results and indicators
mobilitaetscheckEingabe_user_assoziation = Table(
    "mobilitaetscheckEingabe_user",
    Base.metadata,
    Column(
        "user_id",
        GUID,
        ForeignKey("user.id", ondelete="CASCADE"),
    ),
    Column(
        "mobilitaetscheck_eingabe_id",
        Integer,
        ForeignKey("mobilitaetscheck_eingabe.id", ondelete="CASCADE"),
    ),
)
