import unittest
from backend.application.employee.services import EmployeeApplicationService
from backend.application.employee.dto import CreateEmployeeRequest
from backend.application.shared.interfaces import EmployeeRepository

class InMemoryEmployeeRepository(EmployeeRepository):
    def __init__(self):
        self.db = {}

    def save(self, employee):
        self.db[employee.id] = employee

    def find_by_id(self, id):
        return self.db.get(id)

class TestEmployee(unittest.TestCase):
    def test_create_employee(self):
        repo = InMemoryEmployeeRepository()
        service = EmployeeApplicationService(repo)
        
        req = CreateEmployeeRequest(id="emp-1", name="Amani", role="Stylist", branch_id="b1", user_role="Manager")
        res = service.create_employee(req)
        
        self.assertEqual(res.id, "emp-1")
        self.assertEqual(res.role, "Stylist")
        self.assertFalse(res.is_suspended)

    def test_assign_branch(self):
        repo = InMemoryEmployeeRepository()
        service = EmployeeApplicationService(repo)
        
        service.create_employee(CreateEmployeeRequest("emp-1", "Amani", "Stylist", "b1", "Manager"))
        res = service.assign_branch("emp-1", "b2", "Manager")
        self.assertEqual(res.branch_id, "b2")

    def test_change_role(self):
        repo = InMemoryEmployeeRepository()
        service = EmployeeApplicationService(repo)
        
        service.create_employee(CreateEmployeeRequest("emp-1", "Amani", "Stylist", "b1", "Manager"))
        res = service.change_role("emp-1", "Lead Stylist", "Manager")
        self.assertEqual(res.role, "Lead Stylist")

    def test_suspend_and_activate_employee(self):
        repo = InMemoryEmployeeRepository()
        service = EmployeeApplicationService(repo)
        
        service.create_employee(CreateEmployeeRequest("emp-1", "Amani", "Stylist", "b1", "Manager"))
        res = service.suspend_employee("emp-1", "Manager")
        self.assertTrue(res.is_suspended)
        
        res = service.activate_employee("emp-1", "Manager")
        self.assertFalse(res.is_suspended)

if __name__ == '__main__':
    unittest.main()
