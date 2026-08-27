from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class State_log(Base):
    __tablename__ = "state_log"

    device_id: Mapped[str] = mapped_column(
        String(24),
        ForeignKey("devices.device_id"),
        primary_key=True,
    )

    state: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        server_default="not_used",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )