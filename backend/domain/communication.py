import time
from typing import Dict

class MessageTemplate:
    def __init__(self, name: str, language: str, body: str):
        self.name = name
        self.language = language
        self.body = body  # e.g. "مرحباً {customer_name}، نؤكد موعدك في {time_slot}."

    def render(self, variables: Dict[str, str]) -> str:
        rendered = self.body
        for key, val in variables.items():
            rendered = rendered.replace(f"{{{key}}}", str(val))
        return rendered

class MessageLog:
    def __init__(self, id: str, recipient: str, channel: str, content: str, status: str = "queued"):
        self.id = id
        self.recipient = recipient
        self.channel = channel  # WhatsApp, SMS, Email, Push
        self.content = content
        self.status = status  # queued, delivered, opened, clicked, failed
        self.timestamp = int(time.time())

class Campaign:
    def __init__(self, id: str, name: str, template_name: str, target_tier: str = "VIP"):
        self.id = id
        self.name = name
        self.template_name = template_name
        self.target_tier = target_tier
