from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.seat_allocation import SeatAllocation

from sqlalchemy import DateTime, Enum, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.enums import SeatStatus


class Seat(Base):
    __tablename__ = "seats"

    __table_args__ = (
        UniqueConstraint(
            "floor",
            "zone",
            "seat_number",
            name="uq_floor_zone_seat"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    floor: Mapped[int] = mapped_column(nullable=False)

    zone: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    bay: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    seat_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[SeatStatus] = mapped_column(
        Enum(SeatStatus),
        default=SeatStatus.AVAILABLE,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    allocations: Mapped[List["SeatAllocation"]] = relationship(
        back_populates="seat",
        cascade="all, delete-orphan"
    )