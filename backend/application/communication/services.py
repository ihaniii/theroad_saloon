import uuid
from typing import List, Dict
from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import CustomerRepository
from backend.domain.communication import MessageTemplate, MessageLog, Campaign
from backend.application.communication.dto import SendMessageRequest, MessageLogResponse, CreateCampaignRequest, CampaignResponse

class CommunicationApplicationService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
        self.logs: List[MessageLog] = []
        self.campaigns: List[Campaign] = []
        
        # Prepopulate localization templates
        self.templates = {
            "confirm_appt_ar": MessageTemplate("confirm_appt_ar", "ar", "مرحباً {customer_name}، نؤكد موعدك في {time_slot}."),
            "confirm_appt_en": MessageTemplate("confirm_appt_en", "en", "Hello {customer_name}, we confirm your booking at {time_slot}."),
            "birthday_greet_ar": MessageTemplate("birthday_greet_ar", "ar", "كل عام وأنتِ بخير {customer_name}! نقدم لكِ خصم خاص اليوم."),
            "birthday_greet_en": MessageTemplate("birthday_greet_en", "en", "Happy Birthday {customer_name}! We have a special discount for you today.")
        }

    def send_message(self, req: SendMessageRequest) -> MessageLogResponse:
        Authorizer.check_permission(req.user_role, "SearchCustomers")
        
        template = self.templates.get(req.template_name)
        if not template:
            raise ValueError(f"Template '{req.template_name}' not found.")
            
        content = template.render(req.variables)
        
        # Mock actual API dispatch and write log entry
        log_id = str(uuid.uuid4())
        log_entry = MessageLog(
            id=log_id,
            recipient=req.recipient,
            channel=req.channel,
            content=content,
            status="delivered"  # Success mock state
        )
        self.logs.append(log_entry)
        return self._to_log_response(log_entry)

    def create_campaign(self, req: CreateCampaignRequest) -> CampaignResponse:
        Authorizer.check_permission(req.user_role, "ApplyDiscount") # Manager+
        
        campaign = Campaign(req.id, req.name, req.template_name, req.target_tier)
        self.campaigns.append(campaign)
        
        # Execute campaign blast targeting customers
        customers = self.customer_repo.search("") # search all
        for cust in customers:
            # Check target tier (e.g. VIP)
            is_target = False
            if req.target_tier == "VIP" and "VIP" in cust.loyalty_tier:
                is_target = True
            elif req.target_tier == "ALL" and cust.is_active:
                is_target = True
                
            if is_target:
                # Send the message
                self.send_message(SendMessageRequest(
                    recipient=cust.phone,
                    channel="WhatsApp",
                    template_name=req.template_name,
                    variables={"customer_name": cust.name, "time_slot": "الموعد القادم"},
                    language="ar",
                    user_role=req.user_role
                ))
                
        return self._to_campaign_response(campaign)

    def get_logs(self, user_role: str) -> List[MessageLogResponse]:
        Authorizer.check_permission(user_role, "SearchCustomers")
        return [self._to_log_response(l) for l in self.logs]

    def get_campaigns(self, user_role: str) -> List[CampaignResponse]:
        Authorizer.check_permission(user_role, "SearchCustomers")
        return [self._to_campaign_response(c) for c in self.campaigns]

    def _to_log_response(self, l: MessageLog) -> MessageLogResponse:
        return MessageLogResponse(
            id=l.id,
            recipient=l.recipient,
            channel=l.channel,
            content=l.content,
            status=l.status,
            timestamp=l.timestamp
        )

    def _to_campaign_response(self, c: Campaign) -> CampaignResponse:
        return CampaignResponse(
            id=c.id,
            name=c.name,
            template_name=c.template_name,
            target_tier=c.target_tier
        )
