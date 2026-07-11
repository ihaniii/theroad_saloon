from typing import List, Tuple

class ServiceRecipe:
    def __init__(self, service_name: str, items: List[Tuple[str, int]]):
        self.service_name = service_name
        self.items = items  # List of tuples (product_id, quantity_to_consume)

    def get_requirements(self) -> List[Tuple[str, int]]:
        return self.items
