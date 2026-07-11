from typing import Optional, List
from backend.application.shared.interfaces import InventoryRepository
from backend.domain.inventory import InventoryItem
from backend.infrastructure.database.connection import DbConnection

class SqliteInventoryRepository(InventoryRepository):
    def __init__(self):
        self.conn = DbConnection.get_connection()

    def save(self, item: InventoryItem) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO inventory (id, product_name, quantity, sku, reorder_point, warehouse) VALUES (?, ?, ?, ?, ?, ?)",
            (item.id, item.product_name, item.quantity, item.sku, item.reorder_point, item.warehouse)
        )
        self.conn.commit()

    def find_by_id(self, id: str) -> Optional[InventoryItem]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, product_name, quantity, sku, reorder_point, warehouse FROM inventory WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return InventoryItem(
            id=row["id"],
            product_name=row["product_name"],
            quantity=row["quantity"],
            sku=row["sku"],
            reorder_point=row["reorder_point"],
            warehouse=row["warehouse"]
        )

    def find_all(self) -> List[InventoryItem]:
         cursor = self.conn.cursor()
         cursor.execute("SELECT id, product_name, quantity, sku, reorder_point, warehouse FROM inventory")
         rows = cursor.fetchall()
         return [
             InventoryItem(
                 id=row["id"],
                 product_name=row["product_name"],
                 quantity=row["quantity"],
                 sku=row["sku"],
                 reorder_point=row["reorder_point"],
                 warehouse=row["warehouse"]
             )
             for row in rows
         ]
