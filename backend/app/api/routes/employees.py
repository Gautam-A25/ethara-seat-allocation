from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)

from app.schemas.seat import SeatSuggestionResponse

from app.services.employee_service import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    update_employee,
)

from app.services.seat_service import get_seat_suggestions

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee",
    description="Create a new employee.",
)
def create_employee_route(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return create_employee(db, employee)


@router.get(
    "",
    response_model=List[EmployeeResponse],
    summary="Get All Employees",
    description="Retrieve all employees.",
)
def get_all_employees_route(
    db: Session = Depends(get_db),
):
    return get_all_employees(db)

@router.get(
    "/{employee_id}/seat-suggestions",
    response_model=list[SeatSuggestionResponse],
    summary="Get Seat Suggestions",
)
def get_seat_suggestions_route(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_seat_suggestions(
        db,
        employee_id,
    )

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get Employee",
    description="Retrieve an employee by ID.",
)
def get_employee_route(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_employee(db, employee_id)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update Employee",
    description="Update an existing employee.",
)
def update_employee_route(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    return update_employee(
        db,
        employee_id,
        employee,
    )


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Employee",
    description="Delete an employee.",
)
def delete_employee_route(
    employee_id: int,
    db: Session = Depends(get_db),
):
    delete_employee(db, employee_id)