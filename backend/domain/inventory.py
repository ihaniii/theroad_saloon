class InventoryItem:
    def __init__(self, id: str, product_name: str, quantity: int,
                 sku: str = "", reorder_point: int = 5, warehouse: str = "Main Store"):
        self.id = id
        self.product_name = product_name
        
        if quantity < 0:
            raise ValueError("Inventory stock quantity cannot be negative.")
        self.quantity = quantity
        self.sku = sku
        self.reorder_point = reorder_point
        self.warehouse = warehouse

    def receive_stock(self, amount: int):
        if amount <= 0:
            raise ValueError("Stock increment must be positive.")
        self.quantity += amount

    def adjust(self, new_qty: int):
        if new_qty < 0:
            raise ValueError("Inventory quantity cannot be negative.")
        self.quantity = new_qty

    def consume(self, amount: int):
        if amount <= 0:
            raise ValueError("Consumption amount must be positive.")
        if self.quantity < amount:
            raise ValueError(f"Insufficient stock for {self.product_name}. Available: {self.quantity}, requested: {amount}")
        self.quantity -= amount

    def check_reorder(self) -> bool:
        return self.quantity <= self.reorder_point
