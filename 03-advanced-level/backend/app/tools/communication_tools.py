import httpx
import base64
from ..config.settings import settings
from ..logs.execution_logger import ExecutionLogger
from .gmail_tools import GmailService

class CommunicationTools:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str, thread_id: str = None) -> bool:
        ExecutionLogger.log("Communication", f"Sending email to {to_email}", f"Subject: {subject}")
        return await GmailService.send_email(to_email, subject, body, thread_id)

    @staticmethod
    async def send_whatsapp_message(phone: str, message: str) -> bool:
        ExecutionLogger.log("Communication", f"Sending WhatsApp to {phone}", f"Message: {message[:20]}...")
        
        # Try Twilio first if configured
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            return await CommunicationTools._send_twilio_whatsapp(phone, message)
            
        # Fallback to Ultramsg
        if settings.ULTRAMSG_INSTANCE_ID and settings.ULTRAMSG_TOKEN:
            return await CommunicationTools._send_ultramsg_whatsapp(phone, message)

        ExecutionLogger.log("Communication", "WhatsApp skipped", "No WhatsApp API configured (Twilio or Ultramsg)")
        return False

    @staticmethod
    async def _send_twilio_whatsapp(phone: str, message: str) -> bool:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        # Twilio WhatsApp numbers must be prefixed with 'whatsapp:'
        from_phone = settings.FROM_PHONE_NUMBER or settings.TWILIO_SANDBOX_NUMBER
        if not from_phone.startswith("whatsapp:"):
            from_phone = f"whatsapp:{from_phone}"
            
        to_phone = phone
        if not to_phone.startswith("whatsapp:"):
            to_phone = f"whatsapp:{to_phone}"

        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        auth = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        payload = {
            "From": from_phone,
            "To": to_phone,
            "Body": message
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload, headers=headers)
                if response.status_code in [200, 201]:
                    return True
                else:
                    ExecutionLogger.log("Communication", "Twilio failed", f"Status: {response.status_code}, Body: {response.text}")
                    return False
        except Exception as e:
            ExecutionLogger.log("Communication", "Twilio error", str(e))
            return False

    @staticmethod
    async def _send_ultramsg_whatsapp(phone: str, message: str) -> bool:
        # Normalize phone number (ensure no spaces or extra characters)
        clean_phone = "".join(filter(str.isdigit, phone))
        
        url = f"https://api.ultramsg.com/{settings.ULTRAMSG_INSTANCE_ID}/messages/chat"
        
        payload = {
            "token": settings.ULTRAMSG_TOKEN,
            "to": clean_phone,
            "body": message,
            "priority": 10
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("sent") == "true" or data.get("message") == "ok":
                        return True
                    else:
                        ExecutionLogger.log("Communication", "Ultramsg error", f"Data: {data}")
                        return False
                else:
                    ExecutionLogger.log("Communication", "Ultramsg failed", f"Status: {response.status_code}, Body: {response.text}")
                    return False
        except Exception as e:
            ExecutionLogger.log("Communication", "Ultramsg error", str(e))
            return False

    @staticmethod
    async def notify_admin(message: str) -> bool:
        """Sends a notification to the admin via WhatsApp (for sensitive tasks)"""
        if settings.MY_PHONE_NUMBER:
            return await CommunicationTools.send_whatsapp_message(settings.MY_PHONE_NUMBER, message)
        return False
