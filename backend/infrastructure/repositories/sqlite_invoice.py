from typing import Optional
from backend.application.shared.interfaces import InvoiceRepository
from backend.domain.invoice import Invoice
from backend.infrastructure.database.connection import DbConnection

class SqliteInvoiceRepository(InvoiceRepository):
    def __init__(self):
        self.conn = DbConnection.get_connection()

    def save(self, invoice: Invoice) -> None:
        cursor = self.conn.cursor()
        
        # Save invoice main details
        cursor.execute(
            "INSERT OR REPLACE INTO invoice (id, customer_id, discount, is_paid, payment_method, refunded) VALUES (?, ?, ?, ?, ?, ?)",
            (invoice.id, invoice.customer_id, invoice.discount, 1 if invoice.is_paid else 0, invoice.payment_method, 1 if invoice.refunded else 0)
        )
        
        # Save invoice items
        cursor.execute("DELETE FROM invoice_item WHERE invoice_id = ?", (invoice.id,))
        for item in invoice.items:
            cursor.execute(
                "INSERT INTO invoice_item (invoice_id, item_name, price) VALUES (?, ?, ?)",
                (invoice.id, item[0], item[1])
            )
            
        self.conn.commit()

    def find_by_id(self, id: str) -> Optional[Invoice]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, customer_id, discount, is_paid, payment_method, refunded FROM invoice WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        inv = Invoice(id=row["id"], customer_id=row["customer_id"])
        inv.discount = row["discount"]
        inv.is_paid = True if row["is_paid"] == 1 else False
        inv.payment_method = row["payment_method"]
        inv.refunded = True if row["refunded"] == 1 else False
        
        # Fetch items
        cursor.execute("SELECT item_name, price FROM invoice_item WHERE invoice_id = ?", (id,))
        item_rows = cursor.fetchall()
        for item_row in item_rows:
            inv.items.append((item_row["item_name"], item_row["price"]))
            
        return inv
