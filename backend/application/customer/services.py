from typing import List
from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import CustomerRepository
from backend.application.shared.events import EventPublisher, DomainEvent
from backend.domain.customer import Customer
from backend.application.customer.dto import CreateCustomerRequest, CustomerResponse

class CustomerCreated(DomainEvent):
    def __init__(self, customer_id: str):
        self.customer_id = customer_id

class CustomerMerged(DomainEvent):
    def __init__(self, primary_id: str, duplicate_id: str):
        self.primary_id = primary_id
        self.duplicate_id = duplicate_id

class CustomerApplicationService:
    def __init__(self, repo: CustomerRepository):
        self.repo = repo

    def create_customer(self, req: CreateCustomerRequest) -> CustomerResponse:
        Authorizer.check_permission(req.user_role, "CreateCustomer")
        cust = Customer(
            id=req.id,
            name=req.name,
            phone=req.phone,
            allergies=req.allergies or "",
            preferred_beverage=req.preferred_beverage or "القهوة العربية"
        )
        self.repo.save(cust)
        EventPublisher.publish(CustomerCreated(cust.id))
        return self._to_response(cust)

    def update_customer(self, id: str, name: str, phone: str, allergies: str, preferred_beverage: str, user_role: str) -> CustomerResponse:
        Authorizer.check_permission(user_role, "UpdateCustomer")
        cust = self.repo.find_by_id(id)
        if not cust:
            raise ValueError("Customer not found.")
        cust.update_profile(name, phone, allergies, preferred_beverage)
        self.repo.save(cust)
        return self._to_response(cust)

    def archive_customer(self, id: str, user_role: str) -> CustomerResponse:
        Authorizer.check_permission(user_role, "ArchiveCustomer")
        cust = self.repo.find_by_id(id)
        if not cust:
            raise ValueError("Customer not found.")
        cust.archive()
        self.repo.save(cust)
        return self._to_response(cust)

    def merge_customers(self, primary_id: str, duplicate_id: str, user_role: str) -> CustomerResponse:
        Authorizer.check_permission(user_role, "MergeCustomers")
        primary = self.repo.find_by_id(primary_id)
        duplicate = self.repo.find_by_id(duplicate_id)
        if not primary or not duplicate:
            raise ValueError("One or both customers not found.")
        
        # Call domain merge logic
        primary.merge_with(duplicate)
        
        self.repo.save(primary)
        self.repo.save(duplicate)
        EventPublisher.publish(CustomerMerged(primary.id, duplicate.id))
        return self._to_response(primary)

    def search_customers(self, query: str, user_role: str) -> List[CustomerResponse]:
        Authorizer.check_permission(user_role, "SearchCustomers")
        results = self.repo.search(query)
        return [self._to_response(c) for c in results]

    def add_loyalty_spend(self, id: str, spend: float, user_role: str) -> CustomerResponse:
        Authorizer.check_permission(user_role, "UpdateCustomer")
        cust = self.repo.find_by_id(id)
        if not cust:
            raise ValueError("Customer not found.")
        cust.add_visit(spend)
        self.repo.save(cust)
        return self._to_response(cust)

    def _to_response(self, c: Customer) -> CustomerResponse:
        return CustomerResponse(
            id=c.id,
            name=c.name,
            phone=c.phone,
            is_active=c.is_active,
            allergies=c.allergies,
            preferred_beverage=c.preferred_beverage,
            total_visits=c.total_visits,
            lifetime_value=c.lifetime_value,
            loyalty_points=c.loyalty_points,
            loyalty_tier=c.loyalty_tier
        )
