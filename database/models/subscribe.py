from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Subscribe(Base):
    __tablename__ = "subscribe"

    device_id: Mapped[str] = mapped_column(
        String(24),
        ForeignKey("devices.device_id"),
        primary_key=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("users.user_id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    subscribe_state: Mapped[str] = mapped_column(
        "subscribe-state",
        String(15),
        nullable=False,
        server_default="not_subscribed",
    ) 