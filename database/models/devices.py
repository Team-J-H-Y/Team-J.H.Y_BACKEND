from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

class Devices(Base):
    __tablename__ = "devices"

    device_id: Mapped[str] = mapped_column(
        String(24),
        primary_key=True,
    )