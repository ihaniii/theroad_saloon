class Appointment:
    # State Machine constants
    STATES = ["scheduled", "confirmed", "checked_in", "in_service", "completed", "cancelled", "no_show"]

    def __init__(self, id: str, customer_id: str, employee_id: str, time_slot: str, 
                 start_minute: int, duration_minutes: int, clean_buffer: int = 15,
                 room_id: str = "main_room", chair_id: str = "chair_1", status: str = "scheduled"):
        self.id = id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.time_slot = time_slot
        self.start_minute = start_minute
        self.duration_minutes = duration_minutes
        self.clean_buffer = clean_buffer
        self.room_id = room_id
        self.chair_id = chair_id
        
        if status not in self.STATES:
            raise ValueError(f"Invalid initial status: {status}")
        self.status = status

    def get_total_duration(self) -> int:
        return self.duration_minutes + self.clean_buffer

    def move(self, new_slot: str):
        if self.status in ["cancelled", "completed", "no_show"]:
            raise ValueError("Cannot move a cancelled, completed, or no-show appointment.")
        self.time_slot = new_slot

    def transition_to(self, target_status: str):
        if target_status not in self.STATES:
            raise ValueError(f"Target status '{target_status}' is not a valid state.")
            
        current = self.status
        
        # Validate allowed transitions
        if target_status == "confirmed":
            if current != "scheduled":
                raise ValueError(f"Cannot transition to 'confirmed' from '{current}'")
        elif target_status == "checked_in":
            if current not in ["scheduled", "confirmed"]:
                raise ValueError(f"Cannot transition to 'checked_in' from '{current}'")
        elif target_status == "in_service":
            if current != "checked_in":
                raise ValueError(f"Cannot transition to 'in_service' from '{current}'")
        elif target_status == "completed":
            if current != "in_service":
                raise ValueError(f"Cannot transition to 'completed' from '{current}'")
        elif target_status == "cancelled":
            if current not in ["scheduled", "confirmed"]:
                raise ValueError(f"Cannot cancel appointment when it is '{current}'")
        elif target_status == "no_show":
            if current not in ["scheduled", "confirmed"]:
                raise ValueError(f"Cannot mark as no-show when it is '{current}'")
                
        self.status = target_status
