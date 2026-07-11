from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateCustomerRequest:
    id: str
    name: str
    phone: str
    user_role: str
    allergies: Optional[str] = ""
    preferred_beverage: Optional[str] = "القهوة العربية"

@dataclass
class CustomerResponse:
    id: str
    name: str
    phone: str
    is_active: bool
    allergies: str
    preferred_beverage: str
    total_visits: int
    lifetime_value: float
    loyalty_points: int
    loyalty_tier: str
