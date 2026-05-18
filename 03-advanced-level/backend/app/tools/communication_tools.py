from typing import Dict, Any, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Mock communication services
class MockEmailService:
    async def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        logger.info(f"Mock: Sending email to {recipient} - Subject: {subject}")
        return {"status": "sent", "recipient": recipient, "subject": subject}

class MockWhatsAppService:
    async def send_whatsapp_message(self, recipient_phone: str, message: str) -> Dict[str, Any]:
        logger.info(f"Mock: Sending WhatsApp message to {recipient_phone}")
        return {"status": "sent", "recipient_phone": recipient_phone}

email_service = MockEmailService()
whatsapp_service = MockWhatsAppService()

# --- Email Tools ---
class SendEmailArgs(BaseModel):
    recipient: str = Field(..., description="The email address of the recipient")
    subject: str = Field(..., description="The subject line of the email")
    body: str = Field(..., description="The main content of the email")

@tool(args_schema=SendEmailArgs, tool_name="send_email")
async def send_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Sends an email to a specified recipient.
    Use this to communicate information or updates via email.
    """
    return await email_service.send_email(recipient=recipient, subject=subject, body=body)

# --- WhatsApp Tools ---
class SendWhatsAppMessageArgs(BaseModel):
    recipient_phone: str = Field(..., description="The phone number of the recipient (e.g., '+1234567890')")
    message: str = Field(..., description="The content of the WhatsApp message")

@tool(args_schema=SendWhatsAppMessageArgs, tool_name="send_whatsapp_message")
async def send_whatsapp_message(recipient_phone: str, message: str) -> Dict[str, Any]:
    """
    Sends a WhatsApp message to a specified phone number.
    Use this for real-time notifications or direct communication.
    """
    return await whatsapp_service.send_whatsapp_message(recipient_phone=recipient_phone, message=message)
