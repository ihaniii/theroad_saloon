import unittest
from backend.application.customer.services import CustomerApplicationService, CustomerMerged
from backend.application.customer.dto import CreateCustomerRequest
from backend.application.shared.interfaces import CustomerRepository
from backend.application.shared.events import EventPublisher

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.db = {}

    def save(self, customer):
        self.db[customer.id] = customer

    def find_by_id(self, id):
        return self.db.get(id)

    def search(self, query):
        return [c for c in self.db.values() if query in c.name or query in c.phone]

class TestCustomer(unittest.TestCase):
    def test_create_customer_with_preferences(self):
        repo = InMemoryCustomerRepository()
        service = CustomerApplicationService(repo)
        
        req = CreateCustomerRequest(
            id="c-123",
            name="Aisha",
            phone="96590000000",
            user_role="Reception",
            allergies="Lactose",
            preferred_beverage="قهوة تركية"
        )
        res = service.create_customer(req)
        
        self.assertEqual(res.id, "c-123")
        self.assertEqual(res.allergies, "Lactose")
        self.assertEqual(res.preferred_beverage, "قهوة تركية")
        self.assertEqual(res.loyalty_tier, "عامة")

    def test_loyalty_tier_progression(self):
        repo = InMemoryCustomerRepository()
        service = CustomerApplicationService(repo)
        
        service.create_customer(CreateCustomerRequest("c-1", "Aisha", "9659", "Reception"))
        
        # Add a visit with 600 KWD spend -> Should upgrade to Gold
        res = service.add_loyalty_spend("c-1", 600.0, "Manager")
        self.assertEqual(res.loyalty_tier, "ذهبية VIP")
        self.assertEqual(res.loyalty_points, 600)
        self.assertEqual(res.total_visits, 1)

        # Add another 500 KWD spend (total 1100) -> Should upgrade to Platinum
        res = service.add_loyalty_spend("c-1", 500.0, "Manager")
        self.assertEqual(res.loyalty_tier, "بلاتينية VIP")
        self.assertEqual(res.loyalty_points, 1100)

    def test_merge_profiles(self):
        repo = InMemoryCustomerRepository()
        service = CustomerApplicationService(repo)
        
        service.create_customer(CreateCustomerRequest("c1", "Aisha Primary", "9659", "Reception", allergies="Peanut"))
        service.create_customer(CreateCustomerRequest("c2", "Aisha Duplicate", "9659", "Reception", allergies="Gluten"))
        
        # Add visits to both
        service.add_loyalty_spend("c1", 300.0, "Manager")
        service.add_loyalty_spend("c2", 400.0, "Manager")
        
        events = []
        EventPublisher.clear_subscribers()
        EventPublisher.subscribe("CustomerMerged", lambda e: events.append(e))

        res = service.merge_customers("c1", "c2", "Manager")
        
        # c1 details check
        self.assertEqual(res.id, "c1")
        self.assertEqual(res.total_visits, 2)
        self.assertEqual(res.lifetime_value, 700.0)
        self.assertEqual(res.allergies, "Peanut | Gluten")
        self.assertEqual(res.loyalty_tier, "ذهبية VIP") # 700 points total
        
        # c2 must be archived
        duplicate = repo.find_by_id("c2")
        self.assertFalse(duplicate.is_active)
        
        # Event check
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].primary_id, "c1")

if __name__ == '__main__':
    unittest.main()
