from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, project_data: ProjectCreate) -> Project:
    existing = (
        db.query(Project)
        .filter(Project.name == project_data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project already exists.",
        )

    project = Project(**project_data.model_dump())

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_project(db: Session, project_id: int) -> Project:
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


def get_all_projects(db: Session):
    return db.query(Project).all()


def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate,
) -> Project:

    project = get_project(db, project_id)

    update_data = project_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing = (
            db.query(Project)
            .filter(
                Project.name == update_data["name"],
                Project.id != project_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project name already exists.",
            )

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project_id: int,
) -> None:

    project = get_project(db, project_id)

    db.delete(project)
    db.commit()

def get_project_employees(
    db: Session,
    project_id: int,
):
    # Verify project exists
    get_project(db, project_id)

    return (
        db.query(Employee)
        .filter(Employee.project_id == project_id)
        .all()
    )