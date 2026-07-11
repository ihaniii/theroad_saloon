from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class CreateWorkflowRequest:
    id: str
    trigger_event: str
    conditions: Dict[str, Any]
    actions: List[str]
    user_role: str

@dataclass
class WorkflowResponse:
    id: str
    trigger_event: str
    conditions: Dict[str, Any]
    actions: List[str]
    is_active: bool

@dataclass
class WorkflowHistoryResponse:
    id: str
    rule_id: str
    execution_time: int
    status: str
    errors: str
    retry_count: int
