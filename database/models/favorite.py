from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

class Favorite(Base):
    __tablename__ = "favorite"

    device_id: Mapped[str] = mapped_column(
        String(24),
        ForeignKey("devices.device_id"),
        primary_key=True,
    )
    
    user_id: Mapped[str] = mapped_column(
            String(255),
            ForeignKey("users.user_id"),
            unique=True,
            nullable=False,
    )