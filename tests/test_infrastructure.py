import unittest
import sqlite3
import json
from backend.infrastructure.database.connection import DbConnection
from backend.infrastructure.repositories.sqlite_customer import SqliteCustomerRepository
from backend.infrastructure.repositories.sqlite_appointment import SqliteAppointmentRepository
from backend.domain.customer import Customer
from backend.domain.appointment import Appointment
from backend.infrastructure.auth.jwt_handler import JwtHandler
from backend.infrastructure.logging.structured_log import StructuredLogger
from backend.infrastructure.configuration.config import AppConfig

# Safe import for FastAPI in local test environments
try:
    from backend.infrastructure.api.app import app
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

class TestInfrastructure(unittest.TestCase):

    def setUp(self):
        self.conn = DbConnection.get_connection()

    def test_sqlite_customer_repository_save_and_find(self):
        repo = SqliteCustomerRepository()
        cust = Customer(id="c-999", name="Mariam", phone="9651234567")
        repo.save(cust)
        
        found = repo.find_by_id("c-999")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Mariam")
        self.assertEqual(found.phone, "9651234567")
        self.assertTrue(found.is_active)

    def test_sqlite_appointment_repository_save_and_find(self):
        repo = SqliteAppointmentRepository()
        appt = Appointment(id="a-999", customer_id="c-999", employee_id="e-999", time_slot="2:00 PM", start_minute=600, duration_minutes=60)
        repo.save(appt)
        
        found = repo.find_by_id("a-999")
        self.assertIsNotNone(found)
        self.assertEqual(found.time_slot, "2:00 PM")
        self.assertEqual(found.status, "scheduled")

    def test_jwt_generation_and_verification(self):
        token = JwtHandler.generate_token(user_id="user-123", role="Owner")
        self.assertIsNotNone(token)
        
        payload = JwtHandler.verify_token(token)
        self.assertEqual(payload["sub"], "user-123")
        self.assertEqual(payload["role"], "Owner")

    def test_structured_logger(self):
        StructuredLogger.set_correlation_id("test-corr-id")
        self.assertEqual(StructuredLogger.get_correlation_id(), "test-corr-id")

    def test_app_config_env(self):
        self.assertEqual(AppConfig.ENV, "development")
        self.assertTrue(AppConfig.DEBUG)
        self.assertEqual(AppConfig.get_db_url(), "file:theroad_test_db?mode=memory&cache=shared")

    def test_fastapi_endpoints_declared(self):
        if not HAS_FASTAPI:
            self.skipTest("FastAPI is not installed in the local runtime environment.")
        # Scan routing tables to verify API v1 routes are declared
        routes = [route.path for route in app.routes]
        self.assertIn("/health", routes)
        self.assertIn("/ready", routes)
        self.assertIn("/live", routes)
        self.assertIn("/api/v1/appointments", routes)
        self.assertIn("/api/v1/customers", routes)
        self.assertIn("/api/v1/inventory/receive", routes)
        self.assertIn("/api/v1/invoices", routes)

if __name__ == '__main__':
    unittest.main()
