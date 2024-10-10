from ..database import Base
from sqlalchemy.orm import mapped_column, Mapped

class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]