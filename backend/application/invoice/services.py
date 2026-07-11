from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import InvoiceRepository
from backend.application.shared.events import EventPublisher, DomainEvent
from backend.domain.invoice import Invoice
from backend.application.invoice.dto import CreateInvoiceRequest, RegisterPaymentRequest, IssueRefundRequest, InvoiceResponse

class InvoiceCreated(DomainEvent):
    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id

class InvoicePaid(DomainEvent):
    def __init__(self, invoice_id: str, amount: float):
        self.invoice_id = invoice_id
        self.amount = amount

class PaymentRegistered(DomainEvent):
    def __init__(self, invoice_id: str, method: str, amount: float):
        self.invoice_id = invoice_id
        self.method = method
        self.amount = amount

class RefundIssued(DomainEvent):
    def __init__(self, invoice_id: str, amount: float):
        self.invoice_id = invoice_id
        self.amount = amount

class InvoiceApplicationService:
    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    def create_invoice(self, req: CreateInvoiceRequest) -> InvoiceResponse:
        Authorizer.check_permission(req.user_role, "CreateInvoice")
        inv = Invoice(req.id, req.customer_id)
        self.repo.save(inv)
        EventPublisher.publish(InvoiceCreated(inv.id))
        return self._to_response(inv)

    def add_invoice_item(self, id: str, item_name: str, price: float, user_role: str) -> InvoiceResponse:
        Authorizer.check_permission(user_role, "AddInvoiceItem")
        inv = self.repo.find_by_id(id)
        if not inv:
            raise ValueError("Invoice not found.")
        inv.add_item(item_name, price)
        self.repo.save(inv)
        return self._to_response(inv)

    def remove_invoice_item(self, id: str, item_name: str, user_role: str) -> InvoiceResponse:
        Authorizer.check_permission(user_role, "RemoveInvoiceItem")
        inv = self.repo.find_by_id(id)
        if not inv:
            raise ValueError("Invoice not found.")
        inv.remove_item(item_name)
        self.repo.save(inv)
        return self._to_response(inv)

    def apply_discount(self, id: str, rate: float, user_role: str) -> InvoiceResponse:
        Authorizer.check_permission(user_role, "ApplyDiscount")
        inv = self.repo.find_by_id(id)
        if not inv:
            raise ValueError("Invoice not found.")
        inv.apply_discount(rate)
        self.repo.save(inv)
        return self._to_response(inv)

    def register_payment(self, req: RegisterPaymentRequest) -> InvoiceResponse:
        Authorizer.check_permission(req.user_role, "RegisterPayment")
        inv = self.repo.find_by_id(req.invoice_id)
        if not inv:
            raise ValueError("Invoice not found.")
            
        inv.register_payment(req.method, req.amount)
        self.repo.save(inv)
        
        EventPublisher.publish(PaymentRegistered(inv.id, req.method, req.amount))
        if inv.status == "paid":
            EventPublisher.publish(InvoicePaid(inv.id, inv.get_total()))
            
        return self._to_response(inv)

    def issue_refund(self, req: IssueRefundRequest) -> InvoiceResponse:
        Authorizer.check_permission(req.user_role, "IssueRefund")
        inv = self.repo.find_by_id(req.invoice_id)
        if not inv:
            raise ValueError("Invoice not found.")
            
        inv.issue_refund(req.reason, req.amount)
        self.repo.save(inv)
        
        EventPublisher.publish(RefundIssued(inv.id, req.amount))
        return self._to_response(inv)

    def _to_response(self, inv: Invoice) -> InvoiceResponse:
        return InvoiceResponse(
            id=inv.id,
            customer_id=inv.customer_id,
            items=inv.items,
            discount=inv.discount,
            total=inv.get_total(),
            total_paid=inv.get_total_paid(),
            total_refunded=inv.get_total_refunded(),
            status=inv.status,
            payments=inv.payments,
            refunds=inv.refunds
        )
