from abc import ABC, abstractmethod
from typing import Optional, List
from backend.domain.appointment import Appointment
from backend.domain.customer import Customer
from backend.domain.employee import Employee
from backend.domain.inventory import InventoryItem
from backend.domain.invoice import Invoice

class AppointmentRepository(ABC):
    @abstractmethod
    def save(self, appointment: Appointment) -> None: pass
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Appointment]: pass
    @abstractmethod
    def find_all(self) -> List[Appointment]: pass

class CustomerRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None: pass
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Customer]: pass
    @abstractmethod
    def search(self, query: str) -> List[Customer]: pass

class EmployeeRepository(ABC):
    @abstractmethod
    def save(self, employee: Employee) -> None: pass
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Employee]: pass

class InventoryRepository(ABC):
    @abstractmethod
    def save(self, item: InventoryItem) -> None: pass
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[InventoryItem]: pass

class InvoiceRepository(ABC):
    @abstractmethod
    def save(self, invoice: Invoice) -> None: pass
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Invoice]: pass
