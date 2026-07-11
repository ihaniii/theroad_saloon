import unittest
from backend.application.automation.services import AutomationApplicationService
from backend.application.automation.dto import CreateWorkflowRequest
from backend.application.shared.events import EventPublisher
from backend.application.invoice.services import InvoicePaid

class TestAutomation(unittest.TestCase):

    def test_automation_triggers_on_event_match(self):
        # Create service instance which automatically subscribes to EventPublisher
        service = AutomationApplicationService()
        
        # Define workflow: IF Invoice Paid AND amount > 100, THEN Send WhatsApp
        req = CreateWorkflowRequest(
            id="rule-paid-vip",
            trigger_event="InvoicePaid",
            conditions={"amount_greater_than": 100},
            actions=["Send WhatsApp"],
            user_role="Manager"
        )
        service.create_rule(req)
        
        # Reset event subscribers and re-subscribe automation triggers to avoid duplicate logs in test suite
        EventPublisher.clear_subscribers()
        EventPublisher.subscribe("InvoicePaid", service.handle_invoice_paid)
        
        # Trigger event with amount = 150 (matches condition > 100)
        EventPublisher.publish(InvoicePaid("inv-abc", 150.0))
        
        # Verify success log added to history
        history = service.get_history("Manager")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].rule_id, "rule-paid-vip")
        self.assertEqual(history[0].status, "success")

    def test_automation_skips_on_condition_mismatch(self):
        service = AutomationApplicationService()
        
        req = CreateWorkflowRequest(
            id="rule-paid-vip-2",
            trigger_event="InvoicePaid",
            conditions={"amount_greater_than": 200}, # condition requires > 200
            actions=["Send WhatsApp"],
            user_role="Manager"
        )
        service.create_rule(req)
        
        EventPublisher.clear_subscribers()
        EventPublisher.subscribe("InvoicePaid", service.handle_invoice_paid)
        
        # Trigger event with amount = 150 (fails condition > 200)
        EventPublisher.publish(InvoicePaid("inv-abc", 150.0))
        
        # Verify no execution logs
        history = service.get_history("Manager")
        self.assertEqual(len(history), 0)

if __name__ == '__main__':
    unittest.main()
