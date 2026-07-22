from random import choice
from faker import Faker

from app.database.database import SessionLocal
from app.models.employee import Employee
from app.models.project import Project
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation
from app.models.enums import (
    EmployeeStatus,
    ProjectStatus,
    SeatStatus,
    AllocationStatus,
)

fake = Faker()

NUM_FLOORS = 5
NUM_ZONES = 10
NUM_SEATS = 5500
NUM_EMPLOYEES = 5000
NUM_RESERVED = 100
NUM_PENDING = 50

PROJECT_NAMES = [
    "Indigo",
    "Indreed",
    "Mydreed",
    "Preed",
    "Serfy",
    "Oreed",
    "Bedegreed",
    "Opreed",
    "Serry",
    "Kaary",
]


def main():
    db = SessionLocal()

    try:
        # Clear existing data
        db.query(SeatAllocation).delete()
        db.query(Employee).delete()
        db.query(Seat).delete()
        db.query(Project).delete()
        db.commit()

        # Create projects
        projects = []
        for name in PROJECT_NAMES:
            project = Project(
                name=name,
                description=f"{name} Project",
                manager_name=fake.name(),
                status=ProjectStatus.ACTIVE,
            )
            db.add(project)
            projects.append(project)

        db.commit()

        for project in projects:
            db.refresh(project)

        # Create seats
        zones = [chr(ord("A") + i) for i in range(NUM_ZONES)]
        seats = []

        created = 0
        seat_counter = 1

        while created < NUM_SEATS:
            for floor in range(1, NUM_FLOORS + 1):
                for zone in zones:
                    for bay in range(1, 21):
                        if created >= NUM_SEATS:
                            break

                        seat = Seat(
                            floor=floor,
                            zone=zone,
                            bay=f"B{bay}",
                            seat_number=f"{zone}-{seat_counter:04d}",
                            status=SeatStatus.AVAILABLE,
                        )
                        seats.append(seat)
                        created += 1
                        seat_counter += 1

                    if created >= NUM_SEATS:
                        break
                if created >= NUM_SEATS:
                    break

        db.add_all(seats)
        db.commit()

        # Reserve first 100 seats
        for seat in seats[:NUM_RESERVED]:
            seat.status = SeatStatus.RESERVED
        db.commit()

        # Create employees
        employees = []
        departments = [
            "Engineering",
            "HR",
            "Finance",
            "Operations",
            "Growth",
        ]
        roles = [
            "Developer",
            "Analyst",
            "Manager",
            "QA Engineer",
            "Designer",
        ]

        for i in range(NUM_EMPLOYEES):
            employee = Employee(
                employee_code=f"EMP{i+1:05d}",
                name=fake.name(),
                email=f"user{i+1}@ethara.ai",
                department=choice(departments),
                role=choice(roles),
                joining_date=fake.date_between(start_date="-2y", end_date="today"),
                status=EmployeeStatus.ACTIVE,
                project_id=choice(projects).id,
            )
            employees.append(employee)

        db.add_all(employees)
        db.commit()

        # Allocate seats
        available_seats = [s for s in seats if s.status == SeatStatus.AVAILABLE]
        allocation_count = NUM_EMPLOYEES - NUM_PENDING

        for employee, seat in zip(
            employees[:allocation_count],
            available_seats[:allocation_count],
        ):
            seat.status = SeatStatus.OCCUPIED

            allocation = SeatAllocation(
                employee_id=employee.id,
                seat_id=seat.id,
                project_id=employee.project_id,
                allocation_status=AllocationStatus.ACTIVE,
            )
            db.add(allocation)

        db.commit()

        print("=" * 40)
        print("Seed completed successfully!")
        print("=" * 40)
        print(f"Projects           : {len(projects)}")
        print(f"Seats              : {NUM_SEATS}")
        print(f"Reserved Seats     : {NUM_RESERVED}")
        print(f"Employees          : {NUM_EMPLOYEES}")
        print(f"Allocated Employees: {allocation_count}")
        print(f"Pending Employees  : {NUM_PENDING}")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
