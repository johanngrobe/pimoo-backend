from ..database import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[str]

    municipality_id: Mapped[int] = mapped_column(ForeignKey("municipality.id"))
    municipality: Mapped["Municipality"]= relationship(back_populates="users", lazy="joined")

    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))


from .municipality import Municipality