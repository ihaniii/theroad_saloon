from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import EmployeeRepository
from backend.domain.employee import Employee
from backend.application.employee.dto import CreateEmployeeRequest, EmployeeResponse

class EmployeeApplicationService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def create_employee(self, req: CreateEmployeeRequest) -> EmployeeResponse:
        Authorizer.check_permission(req.user_role, "CreateEmployee")
        emp = Employee(req.id, req.name, req.role, req.branch_id)
        self.repo.save(emp)
        return EmployeeResponse(emp.id, emp.name, emp.role, emp.branch_id, emp.is_suspended)

    def assign_branch(self, id: str, branch_id: str, user_role: str) -> EmployeeResponse:
        Authorizer.check_permission(user_role, "AssignBranch")
        emp = self.repo.find_by_id(id)
        if not emp:
            raise ValueError("Employee not found.")
        emp.assign_branch(branch_id)
        self.repo.save(emp)
        return EmployeeResponse(emp.id, emp.name, emp.role, emp.branch_id, emp.is_suspended)

    def change_role(self, id: str, role: str, user_role: str) -> EmployeeResponse:
        Authorizer.check_permission(user_role, "ChangeRole")
        emp = self.repo.find_by_id(id)
        if not emp:
            raise ValueError("Employee not found.")
        emp.change_role(role)
        self.repo.save(emp)
        return EmployeeResponse(emp.id, emp.name, emp.role, emp.branch_id, emp.is_suspended)

    def suspend_employee(self, id: str, user_role: str) -> EmployeeResponse:
        Authorizer.check_permission(user_role, "SuspendEmployee")
        emp = self.repo.find_by_id(id)
        if not emp:
            raise ValueError("Employee not found.")
        emp.suspend()
        self.repo.save(emp)
        return EmployeeResponse(emp.id, emp.name, emp.role, emp.branch_id, emp.is_suspended)

    def activate_employee(self, id: str, user_role: str) -> EmployeeResponse:
        Authorizer.check_permission(user_role, "ActivateEmployee")
        emp = self.repo.find_by_id(id)
        if not emp:
            raise ValueError("Employee not found.")
        emp.activate()
        self.repo.save(emp)
        return EmployeeResponse(emp.id, emp.name, emp.role, emp.branch_id, emp.is_suspended)
