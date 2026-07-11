from typing import List
from backend.domain.appointment import Appointment

class AvailabilityEngine:

    @staticmethod
    def has_overlap(start_a: int, end_a: int, start_b: int, end_b: int) -> bool:
        # Standard range overlap check: max(start) < min(end)
        return max(start_a, start_b) < min(end_a, end_b)

    @classmethod
    def check_conflicts(cls, proposed: Appointment, existing_appointments: List[Appointment]) -> None:
        p_start = proposed.start_minute
        p_end = p_start + proposed.get_total_duration()

        for ext in existing_appointments:
            # Skip cancelled, completed or no-show bookings as they release resources
            if ext.status in ["cancelled", "completed", "no_show"]:
                continue
            if ext.id == proposed.id:
                continue

            ext_start = ext.start_minute
            ext_end = ext_start + ext.get_total_duration()

            if cls.has_overlap(p_start, p_end, ext_start, ext_end):
                if ext.employee_id == proposed.employee_id:
                    raise ValueError(f"Conflict: Employee '{proposed.employee_id}' is already booked.")
                if ext.room_id == proposed.room_id:
                    raise ValueError(f"Conflict: Room '{proposed.room_id}' is already booked.")
                if ext.chair_id == proposed.chair_id:
                    raise ValueError(f"Conflict: Chair '{proposed.chair_id}' is already booked.")
