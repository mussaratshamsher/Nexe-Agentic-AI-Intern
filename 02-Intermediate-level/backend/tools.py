import os
import json
import logging
from typing import Optional
import resend
from tavily import TavilyClient
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("agent_tools")

# ---------------------------------
# 1. WEB SEARCH TOOL (Tavily)
# ---------------------------------
def web_search(query: str) -> str:
    """Searches the web for the latest information."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: Tavily API key not configured."
    
    try:
        tavily = TavilyClient(api_key=api_key)
        response = tavily.search(query=query, search_depth="basic")
        results = response.get('results', [])
        
        formatted_results = []
        for res in results[:3]: # Top 3 results
            formatted_results.append(f"Title: {res['title']}\nURL: {res['url']}\nContent: {res['content']}\n")
        
        return "\n".join(formatted_results) if formatted_results else "No relevant web results found."
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"Error performing web search: {str(e)}"

# ---------------------------------
# 2. SAVE TO DB TOOL (Firebase Firestore)
# ---------------------------------
# Global variable to hold firestore client
db = None

def init_firebase():
    global db
    if db is not None:
        return db
    
    try:
        # 1. Try environment variable first (for Hugging Face Secrets)
        fb_config = os.getenv("FIREBASE_SERVICE_ACCOUNT")
        if fb_config:
            logger.info("Initializing Firebase from environment variable.")
            cred_dict = json.loads(fb_config)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            return db

        # 2. Fallback to local file (for local development)
        cred_path = os.path.join(os.path.dirname(__file__), "physical-ai-auth.json")
        if os.path.exists(cred_path):
            logger.info("Initializing Firebase from local JSON file.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            return db
        else:
            logger.warning("Neither FIREBASE_SERVICE_ACCOUNT env var nor physical-ai-auth.json found.")
            return None
    except Exception as e:
        logger.error(f"Firebase init error: {e}")
        return None

def save_to_db(collection: str, data: dict) -> str:
    """Saves information to the database."""
    client = init_firebase()
    if not client:
        return "Error: Database not configured. Please add physical-ai-auth.json."
    
    try:
        # Add a timestamp
        data['timestamp'] = firestore.SERVER_TIMESTAMP
        doc_ref = client.collection(collection).add(data)
        return f"Successfully saved to {collection} with ID: {doc_ref[1].id}"
    except Exception as e:
        logger.error(f"DB Save error: {e}")
        return f"Error saving to database: {str(e)}"

# ---------------------------------
# 3. SEND EMAIL TOOL (Resend)
# ---------------------------------
def send_email(to_email: str, subject: str, body: str) -> str:
    """Sends an email summary to the user."""
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        return "Error: Resend API key not configured."
    
    try:
        resend.api_key = api_key
        params = {
            "from": "AI-Assistant <onboarding@resend.dev>", # Default test sender
            "to": [to_email],
            "subject": subject,
            "html": f"<p>{body}</p>",
        }
        email = resend.Emails.send(params)
        return f"Email sent successfully! ID: {email['id']}"
    except Exception as e:
        logger.error(f"Email error: {e}")
        return f"Error sending email: {str(e)}"
