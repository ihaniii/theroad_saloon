from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class SendMessageRequest:
    recipient: str
    channel: str
    template_name: str
    variables: Dict[str, str]
    language: str
    user_role: str

@dataclass
class CreateCampaignRequest:
    id: str
    name: str
    template_name: str
    target_tier: str
    user_role: str

@dataclass
class MessageLogResponse:
    id: str
    recipient: str
    channel: str
    content: str
    status: str
    timestamp: int

@dataclass
class CampaignResponse:
    id: str
    name: str
    template_name: str
    target_tier: str
