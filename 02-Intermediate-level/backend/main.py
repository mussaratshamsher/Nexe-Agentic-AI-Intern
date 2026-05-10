import os
import logging
import json
import uuid
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from openai import AsyncOpenAI
from firebase_admin import firestore

# Import our new tools
from tools import web_search, save_to_db, send_email, init_firebase

# ---------------------------------
# ENV + LOGGING
# ---------------------------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger("rag_agent_backend")

# ---------------------------------
# CONFIG
# ---------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_CLUSTER_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "RAG_AI_TextBook_Data"

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing")

# ---------------------------------
# CLIENTS
# ---------------------------------
llm_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Firebase on startup
init_firebase()

# ---------------------------------
# FASTAPI APP
# ---------------------------------
app = FastAPI(title="Multi-Tool Physical AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# SCHEMAS
# ---------------------------------
class QueryRequest(BaseModel):
    question: str
    user_email: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    tool_used: str

# ---------------------------------
# AGENT TOOLS DEFINITION
# ---------------------------------
def get_book_context(question: str) -> Dict[str, Any]:
    """Search the local textbook vector store."""
    try:
        query_vector = embedding_model.encode(question).tolist()
        search_result = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=3,
            with_payload=True,
        )
        hits = [p for p in search_result.points if p.score >= 0.35]
        if not hits:
            return {"context": "", "sources": []}
        
        contexts = []
        sources = set()
        for h in hits:
            payload = h.payload or {}
            contexts.append(payload.get("text", ""))
            sources.add(payload.get("source", "unknown"))
            
        return {"context": "\n\n".join(contexts), "sources": list(sources)}
    except Exception as e:
        logger.error(f"Book search error: {e}")
        return {"context": "", "sources": []}

# ---------------------------------
# ROUTES
# ---------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
async def agent_query(req: QueryRequest):
    """The main Agent loop that decides which tool to use."""
    
    # Step 1: Get Context from Book
    book_data = get_book_context(req.question)
    
    # Step 2: System Prompt for the Agent
    system_prompt = f"""
You are the 'Physical AI Assistant'. You have access to a textbook and several tools.

AVAILABLE TOOLS:
1. Textbook Context: Use this first.
2. Web Search: Use if the textbook doesn't have the answer or if the user asks for 'latest' info.
3. Save to DB: Use if the user asks to 'remember' or 'save' something.
4. Send Email: Use if the user asks to 'email' the info.

CURRENT TEXTBOOK CONTEXT:
{book_data['context']}

INSTRUCTIONS:
- If the textbook context is sufficient, answer using it.
- If not, you MUST mention you are searching the web and I will provide the search tool result in the next turn (Simulation).
- ALWAYS be professional.
"""

    # For this implementation, we will use a "Single-Turn Decision" logic
    # In a full LangGraph setup this would be multi-turn, but for this Intermediate level, 
    # we will trigger tools based on intent detection.
    
    intent = req.question.lower()
    tool_used = "Textbook"
    final_answer = ""
    sources = book_data['sources']

    if "search" in intent or "latest" in intent or not book_data['context']:
        tool_used = "Web Search"
        web_results = web_search(req.question)
        final_answer = f"I couldn't find a complete answer in the textbook, so I searched the web:\n\n{web_results}"
    
    elif "save" in intent or "remember" in intent:
        tool_used = "Firebase DB"
        status = save_to_db("user_notes", {"note": req.question, "user": req.user_email or "anonymous"})
        final_answer = f"I have saved that information to the database for you. {status}"
        
    elif "email" in intent:
        tool_used = "Resend Email"
        
        # Check if a specific email is mentioned in the question
        import re
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', req.question)
        target_email = email_match.group(0) if email_match else req.user_email
        
        if not target_email:
            final_answer = "I'd love to email that to you, but I don't have a recipient email address. Please provide one!"
        else:
            # Extract content if it's a specific "Email this content to..." request
            content_match = re.search(r'content to [\w\.-]+@[\w\.-]+\.\w+:\s*(.*)', req.question, re.IGNORECASE | re.DOTALL)
            if content_match:
                extracted_content = content_match.group(1).strip()
            else:
                # Fallback to the whole question if not in the expected format
                extracted_content = req.question

            # Limit content to ~400 words to avoid "too long" errors
            words = extracted_content.split()
            if len(words) > 400:
                extracted_content = " ".join(words[:400]) + "..."
                logger.info("Truncated email content to 400 words.")

            email_body = (
                f"Hello,\n\n"
                f"Here is the information you requested from the Physical AI Assistant:\n\n"
                f"--------------------------------------------------\n"
                f"{extracted_content}\n"
                f"--------------------------------------------------\n\n"
                f"Best regards,\n"
                f"Physical AI Agent"
            )
            
            status = send_email(target_email, "AI Assistant Info", email_body)
            
            if "successfully" in status.lower():
                final_answer = f"I've successfully sent the information to {target_email}!"
            else:
                final_answer = f"I tried to send the email to {target_email}, but I ran into an issue: {status}. " \
                               f"Note: If you're using a trial Resend account, you can only send to your own registered email."
    
    else:
        # Standard RAG Answer
        try:
            completion = await llm_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": req.question}
                ],
                temperature=0.1,
            )
            final_answer = completion.choices[0].message.content
        except Exception as e:
            final_answer = f"Error generating answer: {str(e)}"

    return QueryResponse(
        answer=final_answer,
        sources=sources if tool_used == "Textbook" else [],
        tool_used=tool_used
    )

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), user_email: Optional[str] = Form(None)):
    """Dynamically upload and embed a new document and save metadata."""
    try:
        content = await file.read()
        text = content.decode("utf-8")
        
        # Simple embedding and upsert
        vector = embedding_model.encode(text).tolist()
        from qdrant_client.models import PointStruct
        
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": text, "source": file.filename, "user": user_email or "anonymous"}
            )]
        )
        
        # Save metadata to Firestore for visibility
        save_to_db("uploaded_files", {
            "filename": file.filename,
            "user": user_email or "anonymous",
            "size": len(content),
            "type": file.content_type,
            "category": "Reference",
            "status": "Processed",
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        return {"status": "success", "message": f"Uploaded and indexed {file.filename}"}
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files(user_email: Optional[str] = None):
    """Retrieve a list of uploaded files from Firestore."""
    client = init_firebase()
    if not client:
        logger.error("Firebase not initialized")
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        logger.info(f"Fetching files for user: {user_email}")
        query = client.collection("uploaded_files")
        if user_email:
            query = query.where("user", "==", user_email)
        
        # Temporarily removing order_by to avoid index issues
        docs = query.limit(20).stream()
        files = []
        for doc in docs:
            d = doc.to_dict()
            # Convert timestamp to string
            if "timestamp" in d and d["timestamp"]:
                try:
                    d["timestamp"] = d["timestamp"].isoformat()
                except:
                    d["timestamp"] = str(d["timestamp"])
            files.append(d)
            
        logger.info(f"Found {len(files)} files for {user_email}")
        return {"files": files}
    except Exception as e:
        logger.error(f"List files error: {e}")
        return {"files": [], "error": str(e)}

