from typing import Optional, List
from backend.application.shared.interfaces import AppointmentRepository
from backend.domain.appointment import Appointment
from backend.infrastructure.database.connection import DbConnection

class SqliteAppointmentRepository(AppointmentRepository):
    def __init__(self):
        self.conn = DbConnection.get_connection()

    def save(self, appointment: Appointment) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO appointment (id, customer_id, employee_id, time_slot, status, checked_in, start_minute, duration_minutes, clean_buffer, room_id, chair_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (appointment.id, appointment.customer_id, appointment.employee_id, appointment.time_slot, appointment.status, 
             1 if appointment.status == "checked_in" else 0, appointment.start_minute, appointment.duration_minutes, 
             appointment.clean_buffer, appointment.room_id, appointment.chair_id)
        )
        self.conn.commit()

    def find_by_id(self, id: str) -> Optional[Appointment]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, customer_id, employee_id, time_slot, status, checked_in, start_minute, duration_minutes, clean_buffer, room_id, chair_id FROM appointment WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Appointment(
            id=row["id"],
            customer_id=row["customer_id"],
            employee_id=row["employee_id"],
            time_slot=row["time_slot"],
            start_minute=row["start_minute"],
            duration_minutes=row["duration_minutes"],
            clean_buffer=row["clean_buffer"],
            room_id=row["room_id"],
            chair_id=row["chair_id"],
            status=row["status"]
        )

    def find_all(self) -> List[Appointment]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, customer_id, employee_id, time_slot, status, checked_in, start_minute, duration_minutes, clean_buffer, room_id, chair_id FROM appointment")
        rows = cursor.fetchall()
        return [
            Appointment(
                id=row["id"],
                customer_id=row["customer_id"],
                employee_id=row["employee_id"],
                time_slot=row["time_slot"],
                start_minute=row["start_minute"],
                duration_minutes=row["duration_minutes"],
                clean_buffer=row["clean_buffer"],
                room_id=row["room_id"],
                chair_id=row["chair_id"],
                status=row["status"]
            )
            for row in rows
        ]
