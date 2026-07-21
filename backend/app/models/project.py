from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.enums import ProjectStatus

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.seat_allocation import SeatAllocation


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    manager_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.ACTIVE,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    employees: Mapped[List["Employee"]] = relationship(
        back_populates="project"
    )

    allocations: Mapped[List["SeatAllocation"]] = relationship(
        back_populates="project"
    )