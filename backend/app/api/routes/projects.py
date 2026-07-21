from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.employee import EmployeeResponse
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import (
    create_project,
    delete_project,
    get_all_projects,
    get_project,
    get_project_employees,
    update_project,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Project",
)
def create_project_route(
    project: ProjectCreate,
    db: Session = Depends(get_db),
):
    return create_project(db, project)


@router.get(
    "",
    response_model=List[ProjectResponse],
    summary="Get All Projects",
)
def get_all_projects_route(
    db: Session = Depends(get_db),
):
    return get_all_projects(db)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get Project",
)
def get_project_route(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_project(db, project_id)

@router.get(
    "/{project_id}/employees",
    response_model=list[EmployeeResponse],
    summary="Get Employees in Project",
)
def get_project_employees_route(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_project_employees(
        db,
        project_id,
    )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update Project",
)
def update_project_route(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
):
    return update_project(
        db,
        project_id,
        project,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Project",
)
def delete_project_route(
    project_id: int,
    db: Session = Depends(get_db),
):
    delete_project(db, project_id)