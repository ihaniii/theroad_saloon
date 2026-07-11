import unittest
from backend.application.invoice.services import InvoiceApplicationService, InvoicePaid
from backend.application.invoice.dto import CreateInvoiceRequest, RegisterPaymentRequest, IssueRefundRequest
from backend.application.shared.interfaces import InvoiceRepository
from backend.application.shared.events import EventPublisher
from backend.domain.package import PackageLedger

class InMemoryInvoiceRepository(InvoiceRepository):
    def __init__(self):
        self.db = {}

    def save(self, invoice):
        self.db[invoice.id] = invoice

    def find_by_id(self, id):
        return self.db.get(id)

class TestInvoice(unittest.TestCase):
    def test_create_invoice(self):
        repo = InMemoryInvoiceRepository()
        service = InvoiceApplicationService(repo)
        
        req = CreateInvoiceRequest(id="inv-1", customer_id="c1", user_role="Reception")
        res = service.create_invoice(req)
        
        self.assertEqual(res.id, "inv-1")
        self.assertEqual(res.status, "draft")

    def test_add_and_remove_invoice_item(self):
        repo = InMemoryInvoiceRepository()
        service = InvoiceApplicationService(repo)
        
        service.create_invoice(CreateInvoiceRequest("inv-1", "c1", "Reception"))
        service.add_invoice_item("inv-1", "Hair Styling", 50.0, "Reception")
        res = service.add_invoice_item("inv-1", "Manicure", 15.0, "Reception")
        
        self.assertEqual(len(res.items), 2)
        self.assertEqual(res.total, 65.0)
        
        res = service.remove_invoice_item("inv-1", "Manicure", "Reception")
        self.assertEqual(len(res.items), 1)
        self.assertEqual(res.total, 50.0)

    def test_split_payment_process(self):
        repo = InMemoryInvoiceRepository()
        service = InvoiceApplicationService(repo)
        
        service.create_invoice(CreateInvoiceRequest("inv-1", "c1", "Reception"))
        service.add_invoice_item("inv-1", "Balayage", 100.0, "Reception")
        
        events = []
        EventPublisher.clear_subscribers()
        EventPublisher.subscribe("PaymentRegistered", lambda e: events.append(e))

        # Register first split payment (40 KWD) -> status: partially_paid
        res = service.register_payment(RegisterPaymentRequest("inv-1", "Cash", 40.0, "Reception"))
        self.assertEqual(res.status, "partially_paid")
        self.assertEqual(res.total_paid, 40.0)
        self.assertEqual(len(events), 1)

        # Register final payment (60 KWD) -> status: paid
        res = service.register_payment(RegisterPaymentRequest("inv-1", "K-Net", 60.0, "Reception"))
        self.assertEqual(res.status, "paid")
        self.assertEqual(res.total_paid, 100.0)

    def test_refund_limits(self):
        repo = InMemoryInvoiceRepository()
        service = InvoiceApplicationService(repo)
        
        service.create_invoice(CreateInvoiceRequest("inv-1", "c1", "Reception"))
        service.add_invoice_item("inv-1", "Hydrafacial", 120.0, "Reception")
        service.register_payment(RegisterPaymentRequest("inv-1", "K-Net", 120.0, "Reception"))
        
        # Test refunding more than paid -> should fail
        with self.assertRaises(ValueError):
            service.issue_refund(IssueRefundRequest("inv-1", "Unhappy customer", 150.0, "Manager"))

        # Refund 50 KWD -> should succeed (partial refund, status remains paid)
        res = service.issue_refund(IssueRefundRequest("inv-1", "Double charge", 50.0, "Manager"))
        self.assertEqual(res.total_refunded, 50.0)
        self.assertEqual(res.status, "paid")

        # Refund remaining 70 KWD -> should succeed (full refund, status becomes refunded)
        res = service.issue_refund(IssueRefundRequest("inv-1", "Full Refund", 70.0, "Manager"))
        self.assertEqual(res.total_refunded, 120.0)
        self.assertEqual(res.status, "refunded")

    def test_package_ledgers(self):
        pkg = PackageLedger(id="pkg-1", customer_id="c1", package_name="Massage Pac", total_sessions=3)
        
        pkg.redeem_session()
        self.assertEqual(pkg.remaining_sessions, 2)
        
        pkg.freeze()
        with self.assertRaises(ValueError):
            pkg.redeem_session()
            
        pkg.unfreeze()
        pkg.redeem_session()
        pkg.redeem_session()
        self.assertEqual(pkg.remaining_sessions, 0)
        
        # No sessions remaining to redeem -> should fail
        with self.assertRaises(ValueError):
            pkg.redeem_session()

if __name__ == '__main__':
    unittest.main()
