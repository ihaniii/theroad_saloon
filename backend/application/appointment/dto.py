from dataclasses import dataclass

@dataclass
class CreateAppointmentRequest:
    id: str
    customer_id: str
    employee_id: str
    time_slot: str
    start_minute: int
    duration_minutes: int
    room_id: str
    chair_id: str
    user_role: str
    clean_buffer: int = 15

@dataclass
class AppointmentResponse:
    id: str
    customer_id: str
    employee_id: str
    time_slot: str
    start_minute: int
    duration_minutes: int
    clean_buffer: int
    room_id: str
    chair_id: str
    status: str
