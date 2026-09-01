from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column


from database.base import Base

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    # image: Mapped[bytes] = mapped_column(
    #     LargeBinary,
    #     nullable=True,
    # )

    image: Mapped[str] = mapped_column(
            String(500),
            nullable=True,
    )

    email: Mapped[str] = mapped_column(
            String(255),
            nullable=False,
            unique=True
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


    number: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        unique=True
    )
"""
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )
"""