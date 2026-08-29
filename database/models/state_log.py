from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, BigInteger,func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class State_log(Base):
    __tablename__ = "state_log"

    state_log_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    device_id: Mapped[str] = mapped_column(
        String(24),
        ForeignKey("devices.device_id"),
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