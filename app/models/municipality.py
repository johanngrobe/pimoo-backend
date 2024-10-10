from ..database import Base
from sqlalchemy.orm import mapped_column, Mapped

class Municipality(Base):
    __tablename__ = "municipality"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    name: Mapped[str]