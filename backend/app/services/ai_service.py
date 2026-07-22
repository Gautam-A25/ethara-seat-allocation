import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

from app.database.database import SessionLocal
from app.services.ai_db import (
    get_employee_seat,
    get_available_seats,
    get_employee_project,
    get_dashboard_data,
    get_project_seating,
    get_project_manager,
    get_floor_employees,
    get_all_project_names,
)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(os.getenv("MODEL"))


def process_ai_query(query: str) -> str:
    db = SessionLocal()

    try:
        q = query.lower()

        # Employee seat lookup
        if (
            ("seat" in q or "sit" in q or "sitting" in q)
            and "emp" in q
        ):
            match = re.search(r"emp\d+", q, re.IGNORECASE)

            if match:
                employee_code = match.group(0).upper()

                result = get_employee_seat(db, employee_code)

                if not result:
                    return "Employee or active seat allocation not found."

                return (
                    f"{result['employee']} ({result['employee_code']}) "
                    f"is sitting at Seat {result['seat']}, "
                    f"Bay {result['bay']}, "
                    f"Zone {result['zone']}, "
                    f"Floor {result['floor']} "
                    f"for project {result['project']}."
                )

        # Available seats
        if "available" in q and "seat" in q:

            floor = None

            match = re.search(r"floor\s*(\d+)", q)

            if match:
                floor = int(match.group(1))

            seats = get_available_seats(db, floor)

            if not seats:
                return "No available seats found."

            answer = "Available Seats:\n\n"

            for seat in seats:
                answer += (
                    f"• Floor {seat['floor']} | "
                    f"Zone {seat['zone']} | "
                    f"Bay {seat['bay']} | "
                    f"Seat {seat['seat']}\n"
                )

            return answer
        
        # Employee project lookup
        if "project" in q and "emp" in q:

            match = re.search(r"emp\d+", q, re.IGNORECASE)

            if match:
                employee_code = match.group(0).upper()

                result = get_employee_project(db, employee_code)

                if not result:
                    return "Employee not found."

                return (
                    f"{result['employee']} ({result['employee_code']}) "
                    f"is currently assigned to project "
                    f"{result['project']}."
                )
            
        # Project seating lookup
        if (
            ("project" in q)
            and (
                "seat" in q
                or "sit" in q
                or "employee" in q
                or "people" in q
            )
        ):

            project_name = None

            for name in get_all_project_names(db):
                if name.lower() in q:
                    project_name = name
                    break

            if project_name:

                result = get_project_seating(db, project_name)

                if not result:
                    return "No active employees found for that project."

                answer = f"Employees in project {project_name}:\n\n"

                for emp in result:
                    answer += (
                        f"• {emp['employee']} ({emp['employee_code']})"
                        f" → Seat {emp['seat']} | "
                        f"Floor {emp['floor']} | "
                        f"Zone {emp['zone']} | "
                        f"Bay {emp['bay']}\n"
                    )

                return answer


        # Project manager lookup
        if (
            "project" in q
            and (
                "manager" in q
                or "manage" in q
                or "manages" in q
                or "managed by" in q
                or "lead" in q
                or "owner" in q
            )
        ):

            project_name = None

            for name in get_all_project_names(db):
                if name.lower() in q:
                    project_name = name
                    break

            if project_name:

                result = get_project_manager(db, project_name)

                if result:
                    return (
                        f"{result['project']} is managed by "
                        f"{result['manager']}."
                    )


        # Floor lookup
        if "floor" in q and (
            "who" in q
            or "employee" in q
            or "sit" in q
        ):

            match = re.search(r"floor\s*(\d+)", q)

            if match:

                floor = int(match.group(1))

                employees = get_floor_employees(db, floor)

                if not employees:
                    return "No employees found on that floor."

                answer = f"Employees on Floor {floor}:\n\n"

                for emp in employees:
                    answer += (
                        f"• {emp['employee']} ({emp['employee_code']})"
                        f" — Seat {emp['seat']} "
                        f"({emp['project']})\n"
                    )

                return answer
            
        # Dashboard summary
        if "dashboard" in q or "summary" in q or "statistics" in q:

            summary = get_dashboard_data(db)

            return (
                f"Dashboard Summary:\n\n"
                f"• Total Employees: {summary['total_employees']}\n"
                f"• Total Seats: {summary['total_seats']}\n"
                f"• Occupied Seats: {summary['occupied_seats']}\n"
                f"• Available Seats: {summary['available_seats']}\n"
                f"• Reserved Seats: {summary['reserved_seats']}\n"
                f"• Pending Allocation: {summary['pending_allocation']}\n"
            )

        # Default Gemini response
        response = model.generate_content(query)
        return response.text

    finally:
        db.close()