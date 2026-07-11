from dataclasses import dataclass

@dataclass
class CreateEmployeeRequest:
    id: str
    name: str
    role: str
    branch_id: str
    user_role: str

@dataclass
class EmployeeResponse:
    id: str
    name: str
    role: str
    branch_id: str
    is_suspended: bool
