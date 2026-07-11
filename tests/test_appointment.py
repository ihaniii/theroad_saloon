import unittest
from backend.application.appointment.services import AppointmentApplicationService, AppointmentCreated, AppointmentCancelled, AppointmentCompleted
from backend.application.appointment.dto import CreateAppointmentRequest
from backend.application.shared.interfaces import AppointmentRepository
from backend.application.shared.auth import PermissionError
from backend.application.shared.events import EventPublisher

class InMemoryAppointmentRepository(AppointmentRepository):
    def __init__(self):
        self.db = {}

    def save(self, appointment):
        self.db[appointment.id] = appointment

    def find_by_id(self, id):
        return self.db.get(id)

    def find_all(self):
        return list(self.db.values())

class TestAppointment(unittest.TestCase):
    def test_create_appointment_success(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        events_triggered = []
        EventPublisher.clear_subscribers()
        EventPublisher.subscribe("AppointmentCreated", lambda e: events_triggered.append(e))

        req = CreateAppointmentRequest(
            id="appt-123",
            customer_id="cust-123",
            employee_id="stylist-123",
            time_slot="10:00 AM",
            start_minute=600,
            duration_minutes=60,
            room_id="main_room",
            chair_id="chair_1",
            user_role="Reception"
        )
        
        res = service.create_appointment(req)
        self.assertEqual(res.id, "appt-123")
        self.assertEqual(res.status, "scheduled")
        self.assertEqual(len(events_triggered), 1)

    def test_create_appointment_unauthorized(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        req = CreateAppointmentRequest(
            id="appt-123",
            customer_id="cust-123",
            employee_id="stylist-123",
            time_slot="10:00 AM",
            start_minute=600,
            duration_minutes=60,
            room_id="main_room",
            chair_id="chair_1",
            user_role="Stylist"
        )
        
        with self.assertRaises(PermissionError):
            service.create_appointment(req)

    def test_move_appointment_success(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "s1", "10:00", 600, 60, "main_room", "chair_1", "Reception"))
        res = service.move_appointment("appt-1", "11:00", 660, "Reception")
        self.assertEqual(res.time_slot, "11:00")
        self.assertEqual(res.start_minute, 660)

    def test_move_appointment_conflict(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        # Book appt-1 at 10:00 AM (600) for Stylist 1 (s1)
        service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "s1", "10:00", 600, 60, "main_room", "chair_1", "Reception"))
        # Book appt-2 at 12:00 PM (720) for Stylist 1 (s1)
        service.create_appointment(CreateAppointmentRequest("appt-2", "c2", "s1", "12:00", 720, 60, "main_room", "chair_2", "Reception"))
        
        # Attempt to move appt-2 to 10:30 AM (630), which overlaps with appt-1 (600-675 total total block with buffer)
        with self.assertRaises(ValueError):
            service.move_appointment("appt-2", "10:30", 630, "Reception")

    def test_cancel_appointment(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "s1", "10:00", 600, 60, "main_room", "chair_1", "Reception"))
        events = []
        EventPublisher.subscribe("AppointmentCancelled", lambda e: events.append(e))
        
        res = service.cancel_appointment("appt-1", "Reception")
        self.assertEqual(res.status, "cancelled")
        self.assertEqual(len(events), 1)

    def test_invalid_state_transition(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "s1", "10:00", 600, 60, "main_room", "chair_1", "Reception"))
        
        # Cannot transition directly from scheduled to completed (needs checked_in -> in_service first)
        with self.assertRaises(ValueError):
            service.complete_appointment("appt-1", "Manager")

    def test_check_in_and_complete_workflow(self):
        repo = InMemoryAppointmentRepository()
        service = AppointmentApplicationService(repo)
        
        service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "s1", "10:00", 600, 60, "main_room", "chair_1", "Reception"))
        
        # 1. Check In
        res = service.check_in_customer("appt-1", "Reception")
        self.assertEqual(res.status, "checked_in")
        
        # 2. Complete (automatically transitions checked_in -> in_service -> completed)
        res = service.complete_appointment("appt-1", "Manager")
        self.assertEqual(res.status, "completed")

if __name__ == '__main__':
    unittest.main()
