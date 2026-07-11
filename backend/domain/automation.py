import time
from typing import Dict, List, Any

class WorkflowRule:
    def __init__(self, id: str, trigger_event: str, conditions: Dict[str, Any], actions: List[str], is_active: bool = True):
        self.id = id
        self.trigger_event = trigger_event
        self.conditions = conditions  # e.g. {"membership_tier": "VIP", "amount_greater_than": 100}
        self.actions = actions        # e.g. ["Send WhatsApp", "Award Loyalty"]
        self.is_active = is_active

    def evaluate_conditions(self, context: Dict[str, Any]) -> bool:
        # Loop through defined conditions and check if context matches
        for key, expected in self.conditions.items():
            if key not in context:
                return False
                
            val = context[key]
            if key.endswith("_greater_than"):
                # Handle numeric comparison helpers
                actual_val = context.get(key.replace("_greater_than", ""))
                if actual_val is None or actual_val <= expected:
                    return False
            else:
                if val != expected:
                    return False
        return True

class WorkflowHistory:
    def __init__(self, id: str, rule_id: str, status: str, errors: str = None, retry_count: int = 0):
        self.id = id
        self.rule_id = rule_id
        self.execution_time = int(time.time())
        self.status = status  # success, failed
        self.errors = errors
        self.retry_count = retry_count
