from datetime import datetime

from sqlalchemy import BINARY, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

class Favorite(Base):
    __tablename__ = "favorite"

    device_id: Mapped[str] = mapped_column(
        String(24),
        ForeignKey("devices.device_id"),
        primary_key=True,
    )
    
    user_id: Mapped[bytes] = mapped_column(
            BINARY(16),
            ForeignKey("users.user_id"),
            primary_key=True,
            nullable=False,
            unique=True
    )