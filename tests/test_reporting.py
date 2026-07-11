import unittest
from backend.application.reporting.services import ReportingApplicationService
from backend.application.appointment.services import AppointmentApplicationService
from backend.application.appointment.dto import CreateAppointmentRequest
from backend.application.invoice.services import InvoiceApplicationService
from backend.application.invoice.dto import CreateInvoiceRequest, RegisterPaymentRequest
from backend.application.inventory.services import InventoryApplicationService
from backend.application.inventory.dto import ReceiveStockRequest
from tests.test_appointment import InMemoryAppointmentRepository
from tests.test_customer import InMemoryCustomerRepository
from tests.test_invoice import InMemoryInvoiceRepository
from tests.test_inventory import InMemoryInventoryRepository

class TestReporting(unittest.TestCase):
    def test_dashboard_aggregates_compilation(self):
        appt_repo = InMemoryAppointmentRepository()
        cust_repo = InMemoryCustomerRepository()
        invoice_repo = InMemoryInvoiceRepository()
        inventory_repo = InMemoryInventoryRepository()
        
        appt_service = AppointmentApplicationService(appt_repo)
        invoice_service = InvoiceApplicationService(invoice_repo)
        inventory_service = InventoryApplicationService(inventory_repo)
        
        reporting_service = ReportingApplicationService(
            appt_repo, cust_repo, invoice_repo, inventory_repo
        )

        # 1. Create a complete checked-in appointment and paid invoice
        appt_service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "stylist-1", "10:00 AM", 600, 60, "main_room", "chair_1", "Reception"))
        appt_service.check_in_customer("appt-1", "Reception")
        
        invoice_service.create_invoice(CreateInvoiceRequest("appt-1", "c1", "Reception"))
        invoice_service.add_invoice_item("appt-1", "Hair Cut", 50.0, "Reception")
        invoice_service.register_payment(RegisterPaymentRequest("appt-1", "Cash", 50.0, "Reception"))
        
        # 2. Add inventory item with low stock reorder alert (quantity: 2, reorder: 4)
        inventory_service.receive_stock(ReceiveStockRequest("item-1", "Hydra Mask", 2, "Inventory", reorder_point=4))
        
        # 3. Pull dashboard aggregates
        res = reporting_service.get_dashboard_aggregates("Owner")
        
        self.assertEqual(res.today_revenue, 50.0)
        self.assertEqual(res.active_stylists_count, 1)
        self.assertEqual(res.customers_in_salon, 1)
        self.assertEqual(res.low_stock_alerts_count, 1)

    def test_staff_performance_commission(self):
        appt_repo = InMemoryAppointmentRepository()
        cust_repo = InMemoryCustomerRepository()
        invoice_repo = InMemoryInvoiceRepository()
        inventory_repo = InMemoryInventoryRepository()
        
        appt_service = AppointmentApplicationService(appt_repo)
        invoice_service = InvoiceApplicationService(invoice_repo)
        
        reporting_service = ReportingApplicationService(
            appt_repo, cust_repo, invoice_repo, inventory_repo
        )

        appt_service.create_appointment(CreateAppointmentRequest("appt-1", "c1", "stylist-1", "10:00 AM", 600, 60, "main_room", "chair_1", "Reception"))
        appt_service.check_in_customer("appt-1", "Reception")
        appt_service.complete_appointment("appt-1", "Manager")
        
        invoice_service.create_invoice(CreateInvoiceRequest("appt-1", "c1", "Reception"))
        invoice_service.add_invoice_item("appt-1", "Coloring", 120.0, "Reception")
        invoice_service.register_payment(RegisterPaymentRequest("appt-1", "K-Net", 120.0, "Reception"))
        
        res = reporting_service.get_staff_performance("stylist-1", "Owner")
        self.assertEqual(res.completed_appointments, 1)
        self.assertEqual(res.revenue_generated, 120.0)
        self.assertEqual(res.projected_commission, 12.0) # 10% commission

if __name__ == '__main__':
    unittest.main()
