from typing import Optional
from backend.application.shared.interfaces import EmployeeRepository
from backend.domain.employee import Employee
from backend.infrastructure.database.connection import DbConnection

class SqliteEmployeeRepository(EmployeeRepository):
    def __init__(self):
        self.conn = DbConnection.get_connection()

    def save(self, employee: Employee) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO employee (id, name, role, branch_id, is_suspended) VALUES (?, ?, ?, ?, ?)",
            (employee.id, employee.name, employee.role, employee.branch_id, 1 if employee.is_suspended else 0)
        )
        self.conn.commit()

    def find_by_id(self, id: str) -> Optional[Employee]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, role, branch_id, is_suspended FROM employee WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Employee(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            branch_id=row["branch_id"],
            is_suspended=True if row["is_suspended"] == 1 else False
        )
