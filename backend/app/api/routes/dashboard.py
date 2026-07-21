from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    FloorUtilizationResponse,
    ProjectUtilizationResponse,
)

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_floor_utilization,
    get_project_utilization,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Dashboard Summary",
)
def get_dashboard_summary_route(
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(db)

@router.get(
    "/project-utilization",
    response_model=list[ProjectUtilizationResponse],
    summary="Project Utilization",
)
def get_project_utilization_route(
    db: Session = Depends(get_db),
):
    return get_project_utilization(db)

@router.get(
    "/floor-utilization",
    response_model=list[FloorUtilizationResponse],
    summary="Floor Utilization",
)
def get_floor_utilization_route(
    db: Session = Depends(get_db),
):
    return get_floor_utilization(db)