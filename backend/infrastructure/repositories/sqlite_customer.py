from typing import Optional, List
from backend.application.shared.interfaces import CustomerRepository
from backend.domain.customer import Customer
from backend.infrastructure.database.connection import DbConnection

class SqliteCustomerRepository(CustomerRepository):
    def __init__(self):
        self.conn = DbConnection.get_connection()

    def save(self, customer: Customer) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO customer (id, name, phone, is_active, allergies, preferred_beverage, total_visits, lifetime_value, loyalty_points, loyalty_tier) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (customer.id, customer.name, customer.phone, 1 if customer.is_active else 0,
             customer.allergies, customer.preferred_beverage, customer.total_visits,
             customer.lifetime_value, customer.loyalty_points, customer.loyalty_tier)
        )
        self.conn.commit()

    def find_by_id(self, id: str) -> Optional[Customer]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, phone, is_active, allergies, preferred_beverage, total_visits, lifetime_value, loyalty_points, loyalty_tier FROM customer WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Customer(
            id=row["id"],
            name=row["name"],
            phone=row["phone"],
            is_active=True if row["is_active"] == 1 else False,
            allergies=row["allergies"],
            preferred_beverage=row["preferred_beverage"],
            total_visits=row["total_visits"],
            lifetime_value=row["lifetime_value"],
            loyalty_points=row["loyalty_points"],
            loyalty_tier=row["loyalty_tier"]
        )

    def search(self, query: str) -> List[Customer]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, phone, is_active, allergies, preferred_beverage, total_visits, lifetime_value, loyalty_points, loyalty_tier FROM customer WHERE (name LIKE ? OR phone LIKE ?) AND is_active = 1",
            (f"%{query}%", f"%{query}%")
        )
        rows = cursor.fetchall()
        return [
            Customer(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                is_active=True if row["is_active"] == 1 else False,
                allergies=row["allergies"],
                preferred_beverage=row["preferred_beverage"],
                total_visits=row["total_visits"],
                lifetime_value=row["lifetime_value"],
                loyalty_points=row["loyalty_points"],
                loyalty_tier=row["loyalty_tier"]
            )
            for row in rows
        ]
