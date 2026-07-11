from dataclasses import dataclass
from typing import Optional

@dataclass
class ReceiveStockRequest:
    id: str
    product_name: str
    amount: int
    user_role: str
    sku: Optional[str] = ""
    reorder_point: Optional[int] = 5
    warehouse: Optional[str] = "Main Store"

@dataclass
class TransferStockRequest:
    product_id: str
    source_warehouse: str
    target_warehouse: str
    amount: int
    user_role: str

@dataclass
class InventoryResponse:
    id: str
    product_name: str
    quantity: int
    sku: str
    reorder_point: int
    warehouse: str
