from datetime import date, datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.seat_allocation import SeatAllocation

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.enums import EmployeeStatus


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    employee_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    joining_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(EmployeeStatus),
        default=EmployeeStatus.ACTIVE,
        nullable=False
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    project: Mapped["Project"] = relationship(
        back_populates="employees"
    )

    seat_allocations: Mapped[List["SeatAllocation"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan"
    )