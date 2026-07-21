from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.seat_allocation import (
    SeatAllocationRequest,
    SeatAllocationResponse,
    SeatReleaseRequest,
)

from app.database.dependencies import get_db
from app.schemas.seat import (
    SeatCreate,
    SeatResponse,
    SeatUpdate,
)

from app.services.seat_service import (
    create_seat,
    delete_seat,
    get_all_seats,
    get_available_seats,
    get_seat,
    update_seat,
)

from app.services.seat_allocation_service import (
    allocate_seat,
    release_seat,
)

router = APIRouter(
    prefix="/seats",
    tags=["Seats"],
)


@router.post(
    "",
    response_model=SeatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Seat",
)
def create_seat_route(
    seat: SeatCreate,
    db: Session = Depends(get_db),
):
    return create_seat(db, seat)


@router.get(
    "",
    response_model=List[SeatResponse],
    summary="Get All Seats",
)
def get_all_seats_route(
    db: Session = Depends(get_db),
):
    return get_all_seats(db)


@router.get(
    "/available",
    response_model=List[SeatResponse],
    summary="Get Available Seats",
)
def get_available_seats_route(
    db: Session = Depends(get_db),
):
    return get_available_seats(db)

@router.post(
    "/allocate",
    response_model=SeatAllocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Allocate Seat",
)
def allocate_seat_route(
    allocation: SeatAllocationRequest,
    db: Session = Depends(get_db),
):
    return allocate_seat(
        db,
        allocation,
    )

@router.post(
    "/release",
    response_model=SeatAllocationResponse,
    summary="Release Seat",
)
def release_seat_route(
    release: SeatReleaseRequest,
    db: Session = Depends(get_db),
):
    return release_seat(
        db,
        release,
    )

@router.get(
    "/{seat_id}",
    response_model=SeatResponse,
    summary="Get Seat",
)
def get_seat_route(
    seat_id: int,
    db: Session = Depends(get_db),
):
    return get_seat(db, seat_id)


@router.put(
    "/{seat_id}",
    response_model=SeatResponse,
    summary="Update Seat",
)
def update_seat_route(
    seat_id: int,
    seat: SeatUpdate,
    db: Session = Depends(get_db),
):
    return update_seat(db, seat_id, seat)


@router.delete(
    "/{seat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Seat",
)
def delete_seat_route(
    seat_id: int,
    db: Session = Depends(get_db),
):
    delete_seat(db, seat_id)