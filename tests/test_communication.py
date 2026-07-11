import unittest
from backend.application.communication.services import CommunicationApplicationService
from backend.application.communication.dto import SendMessageRequest, CreateCampaignRequest
from backend.domain.customer import Customer
from tests.test_customer import InMemoryCustomerRepository

class TestCommunication(unittest.TestCase):
    def test_message_rendering(self):
        repo = InMemoryCustomerRepository()
        service = CommunicationApplicationService(repo)
        
        req = SendMessageRequest(
            recipient="96590001122",
            channel="WhatsApp",
            template_name="confirm_appt_ar",
            variables={"customer_name": "دلال", "time_slot": "10:00 ص"},
            language="ar",
            user_role="Reception"
        )
        res = service.send_message(req)
        
        self.assertEqual(res.recipient, "96590001122")
        self.assertEqual(res.channel, "WhatsApp")
        self.assertEqual(res.content, "مرحباً دلال، نؤكد موعدك في 10:00 ص.")
        self.assertEqual(res.status, "delivered")

    def test_campaign_recipient_filtering(self):
        repo = InMemoryCustomerRepository()
        service = CommunicationApplicationService(repo)
        
        # Populate customer base: 1 Gold VIP, 1 regular general member
        repo.save(Customer("c1", "Dalal VIP", "96590000001", loyalty_tier="ذهبية VIP"))
        repo.save(Customer("c2", "Sara General", "96590000002", loyalty_tier="عامة"))
        
        # Launch VIP campaign
        req = CreateCampaignRequest(
            id="camp-vip-offers",
            name="VIP Eid Mubarak Promotion",
            template_name="birthday_greet_ar",
            target_tier="VIP",
            user_role="Manager"
        )
        res = service.create_campaign(req)
        
        self.assertEqual(res.id, "camp-vip-offers")
        self.assertEqual(res.name, "VIP Eid Mubarak Promotion")
        
        # Verify only 1 message sent (matching the Gold VIP customer)
        logs = service.get_logs("Manager")
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].recipient, "96590000001")
        self.assertEqual(logs[0].content, "كل عام وأنتِ بخير Dalal VIP! نقدم لكِ خصم خاص اليوم.")

if __name__ == '__main__':
    unittest.main()
