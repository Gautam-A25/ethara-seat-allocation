from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import Employee
from app.models.project import Project
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    """Create a new employee."""

    # Check duplicate employee code
    if db.query(Employee).filter(
        Employee.employee_code == employee_data.employee_code
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists."
        )

    # Check duplicate email
    if db.query(Employee).filter(
        Employee.email == employee_data.email
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )

    # Verify project exists
    project = db.query(Project).filter(
        Project.id == employee_data.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    employee = Employee(**employee_data.model_dump())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def get_employee(db: Session, employee_id: int) -> Employee:
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    return employee


def get_all_employees(db: Session):
    return db.query(Employee).all()


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee:

    employee = get_employee(db, employee_id)

    update_data = employee_data.model_dump(exclude_unset=True)

    # Validate email uniqueness
    if "email" in update_data:
        existing = db.query(Employee).filter(
            Employee.email == update_data["email"],
            Employee.id != employee_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )

    # Validate project
    if "project_id" in update_data:
        project = db.query(Project).filter(
            Project.id == update_data["project_id"]
        ).first()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found."
            )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(
    db: Session,
    employee_id: int,
) -> None:

    employee = get_employee(db, employee_id)

    db.delete(employee)
    db.commit()