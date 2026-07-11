from typing import List
from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import InventoryRepository
from backend.application.shared.events import EventPublisher, DomainEvent
from backend.domain.inventory import InventoryItem
from backend.domain.recipe import ServiceRecipe
from backend.application.inventory.dto import ReceiveStockRequest, TransferStockRequest, InventoryResponse

class InventoryConsumed(DomainEvent):
    def __init__(self, item_id: str, quantity: int):
        self.item_id = item_id
        self.quantity = quantity

class LowStockDetected(DomainEvent):
    def __init__(self, item_id: str, remaining: int):
        self.item_id = item_id
        self.remaining = remaining

class InventoryApplicationService:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo
        # Predefined recipe database (in-memory mapping)
        self.recipes = {
            "صبغة شعر": ServiceRecipe("صبغة شعر", [("color_tube_1", 1), ("developer_1", 2)]),
            "قص وتسريح شعر": ServiceRecipe("قص وتسريح شعر", [("shampoo_1", 1), ("towels", 1)]),
            "علاج الأظافر المهدئ": ServiceRecipe("علاج الأظافر المهدئ", [("gloves", 1), ("cream_1", 1)])
        }

    def receive_stock(self, req: ReceiveStockRequest) -> InventoryResponse:
        Authorizer.check_permission(req.user_role, "ReceiveStock")
        item = self.repo.find_by_id(req.id)
        if not item:
            item = InventoryItem(req.id, req.product_name, 0, req.sku or "", req.reorder_point or 5, req.warehouse or "Main Store")
        item.receive_stock(req.amount)
        self.repo.save(item)
        return self._to_response(item)

    def adjust_inventory(self, id: str, new_qty: int, user_role: str) -> InventoryResponse:
        Authorizer.check_permission(user_role, "AdjustInventory")
        item = self.repo.find_by_id(id)
        if not item:
            raise ValueError("Inventory item not found.")
        item.adjust(new_qty)
        self.repo.save(item)
        
        # Check reorder alert
        if item.check_reorder():
            EventPublisher.publish(LowStockDetected(item.id, item.quantity))
            
        return self._to_response(item)

    def consume_inventory(self, id: str, amount: int, user_role: str) -> InventoryResponse:
        Authorizer.check_permission(user_role, "ConsumeInventory")
        item = self.repo.find_by_id(id)
        if not item:
            raise ValueError("Inventory item not found.")
        item.consume(amount)
        self.repo.save(item)
        
        EventPublisher.publish(InventoryConsumed(item.id, amount))
        if item.check_reorder():
            EventPublisher.publish(LowStockDetected(item.id, item.quantity))
            
        return self._to_response(item)

    def transfer_stock(self, req: TransferStockRequest) -> InventoryResponse:
        Authorizer.check_permission(req.user_role, "ConsumeInventory") # transfer power
        
        # Fetch items from source and target warehouses
        # For mock, search database by matching product ID and warehouse location
        all_items = self.repo.find_all()
        source_item = next((i for i in all_items if i.id == req.product_id and i.warehouse == req.source_warehouse), None)
        
        if not source_item:
            raise ValueError(f"Product '{req.product_id}' not found in source warehouse '{req.source_warehouse}'.")
            
        # Deduct from source
        source_item.consume(req.amount)
        self.repo.save(source_item)
        
        # Add to target
        target_item = next((i for i in all_items if i.id == req.product_id and i.warehouse == req.target_warehouse), None)
        if not target_item:
            target_item = InventoryItem(
                id=req.product_id,
                product_name=source_item.product_name,
                quantity=0,
                sku=source_item.sku,
                reorder_point=source_item.reorder_point,
                warehouse=req.target_warehouse
            )
        target_item.receive_stock(req.amount)
        self.repo.save(target_item)
        
        return self._to_response(target_item)

    def consume_recipe_for_service(self, service_name: str, user_role: str):
        # Triggered upon appointment complete
        recipe = self.recipes.get(service_name)
        if not recipe:
            return # no recipe mapped for this service, skip
            
        for product_id, qty in recipe.get_requirements():
            self.consume_inventory(product_id, qty, user_role)

    def _to_response(self, i: InventoryItem) -> InventoryResponse:
        return InventoryResponse(
            id=i.id,
            product_name=i.product_name,
            quantity=i.quantity,
            sku=i.sku,
            reorder_point=i.reorder_point,
            warehouse=i.warehouse
        )
