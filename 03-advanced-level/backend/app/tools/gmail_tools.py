import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from ..config.settings import settings
from ..logs.execution_logger import ExecutionLogger

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']

class GmailService:
    _instance = None

    @classmethod
    def get_service(cls):
        if cls._instance is None:
            cls._instance = cls._authenticate()
        return cls._instance

    @staticmethod
    def _authenticate():
        # 1. Handle Cloud Deployment: Write JSON strings from environment to files if provided
        if settings.GMAIL_CREDENTIALS_JSON and not os.path.exists(settings.GMAIL_CREDENTIALS_PATH):
            with open(settings.GMAIL_CREDENTIALS_PATH, 'w') as f:
                f.write(settings.GMAIL_CREDENTIALS_JSON)
        
        if settings.GMAIL_TOKEN_JSON and not os.path.exists(settings.GMAIL_TOKEN_PATH):
            with open(settings.GMAIL_TOKEN_PATH, 'w') as f:
                f.write(settings.GMAIL_TOKEN_JSON)

        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists(settings.GMAIL_TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(settings.GMAIL_TOKEN_PATH, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    ExecutionLogger.log("Gmail", "Failed to refresh token", str(e))
                    creds = None
            
            if not creds:
                if not os.path.exists(settings.GMAIL_CREDENTIALS_PATH):
                    ExecutionLogger.log("Gmail", "Credentials file missing", "Please provide credentials.json or GMAIL_CREDENTIALS_JSON env var")
                    return None
                
                # Check if running in a headless environment (e.g. Docker/HuggingFace)
                is_headless = os.environ.get("HUGGINGFACE_ASSETS_CACHE") or os.environ.get("SPACE_ID")
                if is_headless:
                    ExecutionLogger.log("Gmail", "Auth Failed", "Cannot run local server in headless environment. Please provide a valid GMAIL_TOKEN_JSON.")
                    return None

                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GMAIL_CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(
                    port=8080, 
                    access_type='offline', 
                    prompt='consent'
                )
            
            # Save the credentials for the next run
            with open(settings.GMAIL_TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('gmail', 'v1', credentials=creds, static_discovery=False)
            return service
        except Exception as e:
            ExecutionLogger.log("Gmail", "Failed to build service", str(e))
            return None

    @staticmethod
    async def get_unread_messages():
        service = GmailService.get_service()
        if not service:
            return []

        try:
            results = service.users().messages().list(userId='me', q='is:unread').execute()
            messages = results.get('messages', [])
            
            full_messages = []
            for msg in messages:
                m = service.users().messages().get(userId='me', id=msg['id']).execute()
                
                # Extract subject and sender
                headers = m['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                
                # Extract body
                body = ""
                if 'parts' in m['payload']:
                    for part in m['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            body = base64.urlsafe_b64decode(part['body']['data']).decode()
                            break
                elif 'body' in m['payload']:
                    body = base64.urlsafe_b64decode(m['payload']['body']['data']).decode()

                full_messages.append({
                    'id': msg['id'],
                    'threadId': m['threadId'],
                    'sender': sender,
                    'subject': subject,
                    'body': body
                })
            
            return full_messages
        except Exception as e:
            await ExecutionLogger.log("Gmail", "Error fetching messages", str(e))
            return []

    @staticmethod
    async def send_email(to: str, subject: str, body: str, thread_id: str = None):
        service = GmailService.get_service()
        if not service:
            return False

        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body_dict = {'raw': raw_message}
            if thread_id:
                body_dict['threadId'] = thread_id

            service.users().messages().send(userId='me', body=body_dict).execute()
            await ExecutionLogger.log("Gmail", f"Email sent to {to}", f"Subject: {subject}")
            return True
        except Exception as e:
            await ExecutionLogger.log("Gmail", "Error sending email", str(e))
            return False

    @staticmethod
    async def mark_as_read(message_id: str):
        service = GmailService.get_service()
        if not service:
            return False
        try:
            service.users().messages().batchModify(
                userId='me',
                body={
                    'ids': [message_id],
                    'removeLabelIds': ['UNREAD']
                }
            ).execute()
            return True
        except Exception as e:
            await ExecutionLogger.log("Gmail", "Error marking as read", str(e))
            return False
