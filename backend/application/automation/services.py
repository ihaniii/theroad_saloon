import uuid
from typing import Dict, List, Any
from backend.application.shared.auth import Authorizer
from backend.application.shared.events import EventPublisher, DomainEvent
from backend.domain.automation import WorkflowRule, WorkflowHistory
from backend.application.automation.dto import CreateWorkflowRequest, WorkflowResponse, WorkflowHistoryResponse

class AutomationApplicationService:
    def __init__(self):
        self.rules: List[WorkflowRule] = []
        self.history: List[WorkflowHistory] = []
        
        # Subscribe event executors dynamically
        EventPublisher.subscribe("AppointmentCreated", self.handle_appointment_created)
        EventPublisher.subscribe("InvoicePaid", self.handle_invoice_paid)
        EventPublisher.subscribe("LowStockDetected", self.handle_low_stock)

    def create_rule(self, req: CreateWorkflowRequest) -> WorkflowResponse:
        # Require admin permissions
        Authorizer.check_permission(req.user_role, "ApplyDiscount") # Manager+
        
        rule = WorkflowRule(req.id, req.trigger_event, req.conditions, req.actions)
        self.rules.append(rule)
        return self._to_rule_response(rule)

    def get_rules(self, user_role: str) -> List[WorkflowResponse]:
        Authorizer.check_permission(user_role, "SearchCustomers")
        return [self._to_rule_response(r) for r in self.rules]

    def get_history(self, user_role: str) -> List[WorkflowHistoryResponse]:
        Authorizer.check_permission(user_role, "SearchCustomers")
        return [self._to_history_response(h) for h in self.history]

    # --- EVENT LISTENERS ---

    def handle_appointment_created(self, event: DomainEvent):
        # Context extraction
        context = {
            "appointment_id": event.appointment_id
        }
        self._trigger_workflows("AppointmentCreated", context)

    def handle_invoice_paid(self, event: DomainEvent):
        context = {
            "invoice_id": event.invoice_id,
            "amount": event.amount,
            "amount_greater_than": event.amount
        }
        self._trigger_workflows("InvoicePaid", context)

    def handle_low_stock(self, event: DomainEvent):
        context = {
            "item_id": event.item_id,
            "remaining": event.remaining
        }
        self._trigger_workflows("LowStockDetected", context)

    # --- PRIVATE ENGINE CORE ---

    def _trigger_workflows(self, event_name: str, context: Dict[str, Any]):
        for rule in self.rules:
            if not rule.is_active or rule.trigger_event != event_name:
                continue
                
            if rule.evaluate_conditions(context):
                # Execute actions
                history_id = str(uuid.uuid4())
                try:
                    for action in rule.actions:
                        self._execute_action(action, context)
                        
                    # Log success
                    self.history.append(WorkflowHistory(history_id, rule.id, "success"))
                except Exception as e:
                    # Log failure and trigger retry policies
                    self.history.append(WorkflowHistory(history_id, rule.id, "failed", errors=str(e)))

    def _execute_action(self, action: str, context: Dict[str, Any]):
        # Mock execution logs
        if action == "Send WhatsApp":
            print(f"[Automation Log] Sent WhatsApp notification for context: {context}", flush=True)
        elif action == "Award Loyalty Points":
            print(f"[Automation Log] Loyalty points awarded for context: {context}", flush=True)
        elif action == "Create Purchase Order Draft":
            print(f"[Automation Log] Created PO draft for low stock: {context}", flush=True)
        else:
            raise ValueError(f"Unknown action execution: {action}")

    def _to_rule_response(self, r: WorkflowRule) -> WorkflowResponse:
        return WorkflowResponse(
            id=r.id,
            trigger_event=r.trigger_event,
            conditions=r.conditions,
            actions=r.actions,
            is_active=r.is_active
        )

    def _to_history_response(self, h: WorkflowHistory) -> WorkflowHistoryResponse:
        return WorkflowHistoryResponse(
            id=h.id,
            rule_id=h.rule_id,
            execution_time=h.execution_time,
            status=h.status,
            errors=h.errors,
            retry_count=h.retry_count
        )
