from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(24),
        primary_key=True,
    )

    password_hash: Mapped[str] = mapped_column(
            String(255),
            nullable=False,
            unique=True
    )

    name: Mapped[str] = mapped_column(
        String(24),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )

    number: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        unique=True
    )
