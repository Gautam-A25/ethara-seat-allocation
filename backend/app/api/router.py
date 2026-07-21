from fastapi import APIRouter

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.employees import router as employee_router
from app.api.routes.projects import router as project_router
from app.api.routes.seats import router as seat_router

api_router = APIRouter()

api_router.include_router(project_router)
api_router.include_router(employee_router)
api_router.include_router(seat_router)
api_router.include_router(dashboard_router)