from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import AppointmentRepository
from backend.application.shared.events import EventPublisher, DomainEvent
from backend.domain.appointment import Appointment
from backend.domain.availability import AvailabilityEngine
from backend.application.appointment.dto import CreateAppointmentRequest, AppointmentResponse

class AppointmentCreated(DomainEvent):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id

class AppointmentCancelled(DomainEvent):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id

class AppointmentCompleted(DomainEvent):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id

class AppointmentCheckedIn(DomainEvent):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id

class AppointmentMoved(DomainEvent):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id

class AppointmentNoShow(DomainEvent):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id

class AppointmentApplicationService:
    def __init__(self, repo: AppointmentRepository):
        self.repo = repo

    def create_appointment(self, req: CreateAppointmentRequest) -> AppointmentResponse:
        Authorizer.check_permission(req.user_role, "CreateAppointment")
        
        # Instantiate proposed domain model
        appt = Appointment(
            id=req.id,
            customer_id=req.customer_id,
            employee_id=req.employee_id,
            time_slot=req.time_slot,
            start_minute=req.start_minute,
            duration_minutes=req.duration_minutes,
            clean_buffer=req.clean_buffer,
            room_id=req.room_id,
            chair_id=req.chair_id
        )
        
        # Availability Check
        existing = self.repo.find_all()
        AvailabilityEngine.check_conflicts(appt, existing)
        
        self.repo.save(appt)
        EventPublisher.publish(AppointmentCreated(appt.id))
        return self._to_response(appt)

    def move_appointment(self, id: str, new_slot: str, new_start_minute: int, user_role: str) -> AppointmentResponse:
        Authorizer.check_permission(user_role, "MoveAppointment")
        appt = self.repo.find_by_id(id)
        if not appt:
            raise ValueError("Appointment not found.")
            
        # Update details in domain model
        appt.move(new_slot)
        appt.start_minute = new_start_minute
        
        # Availability Check for the updated parameters
        existing = self.repo.find_all()
        AvailabilityEngine.check_conflicts(appt, existing)
        
        self.repo.save(appt)
        EventPublisher.publish(AppointmentMoved(appt.id))
        return self._to_response(appt)

    def cancel_appointment(self, id: str, user_role: str) -> AppointmentResponse:
        Authorizer.check_permission(user_role, "CancelAppointment")
        appt = self.repo.find_by_id(id)
        if not appt:
            raise ValueError("Appointment not found.")
            
        appt.transition_to("cancelled")
        self.repo.save(appt)
        EventPublisher.publish(AppointmentCancelled(appt.id))
        return self._to_response(appt)

    def complete_appointment(self, id: str, user_role: str) -> AppointmentResponse:
        Authorizer.check_permission(user_role, "CompleteAppointment")
        appt = self.repo.find_by_id(id)
        if not appt:
            raise ValueError("Appointment not found.")
            
        # Checked in -> In Service -> Completed
        if appt.status == "checked_in":
            appt.transition_to("in_service")
        appt.transition_to("completed")
        self.repo.save(appt)
        EventPublisher.publish(AppointmentCompleted(appt.id))
        return self._to_response(appt)

    def check_in_customer(self, id: str, user_role: str) -> AppointmentResponse:
        Authorizer.check_permission(user_role, "CheckInCustomer")
        appt = self.repo.find_by_id(id)
        if not appt:
            raise ValueError("Appointment not found.")
            
        appt.transition_to("checked_in")
        self.repo.save(appt)
        EventPublisher.publish(AppointmentCheckedIn(appt.id))
        return self._to_response(appt)

    def mark_no_show(self, id: str, user_role: str) -> AppointmentResponse:
        # Standardize check
        Authorizer.check_permission(user_role, "CancelAppointment") # equivalent power
        appt = self.repo.find_by_id(id)
        if not appt:
            raise ValueError("Appointment not found.")
            
        appt.transition_to("no_show")
        self.repo.save(appt)
        EventPublisher.publish(AppointmentNoShow(appt.id))
        return self._to_response(appt)

    def _to_response(self, appt: Appointment) -> AppointmentResponse:
        return AppointmentResponse(
            id=appt.id,
            customer_id=appt.customer_id,
            employee_id=appt.employee_id,
            time_slot=appt.time_slot,
            start_minute=appt.start_minute,
            duration_minutes=appt.duration_minutes,
            clean_buffer=appt.clean_buffer,
            room_id=appt.room_id,
            chair_id=appt.chair_id,
            status=appt.status
        )
