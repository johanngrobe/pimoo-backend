from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class UserRolle(Base):
    __tablename__ = "user_rolle"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="User Rolle ID",
    )
    name: Mapped[str] = mapped_column(nullable=False, comment="Name der Benutzerrolle")
    users: Mapped["User"] = relationship(back_populates="rolle", lazy="selectin")


from app.models.user import User
