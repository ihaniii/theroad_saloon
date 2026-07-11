import unittest
from backend.application.inventory.services import InventoryApplicationService, InventoryConsumed, LowStockDetected
from backend.application.inventory.dto import ReceiveStockRequest, TransferStockRequest
from backend.application.shared.interfaces import InventoryRepository
from backend.application.shared.events import EventPublisher

class InMemoryInventoryRepository(InventoryRepository):
    def __init__(self):
        self.db = {}

    def save(self, item):
        # Key by ID + Warehouse combination to support multi-warehouse stubs in tests
        self.db[f"{item.id}_{item.warehouse}"] = item

    def find_by_id(self, id):
        # Return first match from Main Store by default
        return self.db.get(f"{id}_Main Store")

    def find_all(self):
        return list(self.db.values())

class TestInventory(unittest.TestCase):
    def test_receive_stock(self):
        repo = InMemoryInventoryRepository()
        service = InventoryApplicationService(repo)
        
        req = ReceiveStockRequest(id="prod-1", product_name="Teal Hair Oil", amount=10, user_role="Inventory", sku="SKU101", reorder_point=3, warehouse="Main Store")
        res = service.receive_stock(req)
        
        self.assertEqual(res.id, "prod-1")
        self.assertEqual(res.quantity, 10)
        self.assertEqual(res.sku, "SKU101")
        self.assertEqual(res.reorder_point, 3)

    def test_consume_stock_negative_prevention(self):
        repo = InMemoryInventoryRepository()
        service = InventoryApplicationService(repo)
        
        service.receive_stock(ReceiveStockRequest("prod-1", "Teal Hair Oil", 5, "Inventory"))
        
        # Consuming more than available should fail
        with self.assertRaises(ValueError):
            service.consume_inventory("prod-1", 10, "Inventory")

    def test_low_stock_reorder_event(self):
        repo = InMemoryInventoryRepository()
        service = InventoryApplicationService(repo)
        
        service.receive_stock(ReceiveStockRequest("prod-1", "Teal Hair Oil", 10, "Inventory", reorder_point=4))
        
        events = []
        EventPublisher.clear_subscribers()
        EventPublisher.subscribe("LowStockDetected", lambda e: events.append(e))

        # Consume 7 (remaining: 3 -> below reorder point 4)
        service.consume_inventory("prod-1", 7, "Inventory")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].item_id, "prod-1")
        self.assertEqual(events[0].remaining, 3)

    def test_warehouse_transfers(self):
        repo = InMemoryInventoryRepository()
        service = InventoryApplicationService(repo)
        
        # Populate main warehouse
        service.receive_stock(ReceiveStockRequest("prod-1", "Hair Oil", 10, "Inventory", warehouse="Main Store"))
        
        # Transfer 4 to Spa Store
        req = TransferStockRequest("prod-1", "Main Store", "Spa Store", 4, "Inventory")
        res = service.transfer_stock(req)
        
        # Verify target is populated
        self.assertEqual(res.quantity, 4)
        self.assertEqual(res.warehouse, "Spa Store")
        
        # Verify source is decremented
        source = next(i for i in repo.find_all() if i.id == "prod-1" and i.warehouse == "Main Store")
        self.assertEqual(source.quantity, 6)

    def test_service_recipe_consumptions(self):
        repo = InMemoryInventoryRepository()
        service = InventoryApplicationService(repo)
        
        # Prepopulate recipe ingredients
        service.receive_stock(ReceiveStockRequest("color_tube_1", "Color Tube", 10, "Inventory", warehouse="Main Store"))
        service.receive_stock(ReceiveStockRequest("developer_1", "Developer", 10, "Inventory", warehouse="Main Store"))
        
        # Complete coloring service
        service.consume_recipe_for_service("صبغة شعر", "Inventory")
        
        # Verify deductions (Color Tube consumes 1, Developer consumes 2)
        color = repo.find_by_id("color_tube_1")
        dev = repo.find_by_id("developer_1")
        
        self.assertEqual(color.quantity, 9)
        self.assertEqual(dev.quantity, 8)

if __name__ == '__main__':
    unittest.main()
