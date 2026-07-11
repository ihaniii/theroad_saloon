from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CreateInvoiceRequest:
    id: str
    customer_id: str
    user_role: str

@dataclass
class RegisterPaymentRequest:
    invoice_id: str
    method: str
    amount: float
    user_role: str

@dataclass
class IssueRefundRequest:
    invoice_id: str
    reason: str
    amount: float
    user_role: str

@dataclass
class InvoiceResponse:
    id: str
    customer_id: str
    items: List[Tuple[str, float]]
    discount: float
    total: float
    total_paid: float
    total_refunded: float
    status: str
    payments: List[Tuple[str, float]]
    refunds: List[Tuple[str, float]]
