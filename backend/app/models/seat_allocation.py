from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.enums import AllocationStatus

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.project import Project
    from app.models.seat import Seat


class SeatAllocation(Base):
    __tablename__ = "seat_allocations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )

    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.id"),
        nullable=False
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    allocation_status: Mapped[AllocationStatus] = mapped_column(
        Enum(AllocationStatus),
        default=AllocationStatus.ACTIVE,
        nullable=False
    )

    allocation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    released_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="seat_allocations"
    )

    seat: Mapped["Seat"] = relationship(
        back_populates="allocations"
    )

    project: Mapped["Project"] = relationship(
        back_populates="allocations"
    )