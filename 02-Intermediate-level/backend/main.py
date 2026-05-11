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

# Explicitly define allowed origins for production and local development
# Note: When allow_credentials=True, allow_origins cannot be ["*"] in many browsers
allowed_origins = [
    "https://humanoid-robotics-book-sepia.vercel.app",
    "https://physical-ai-book.vercel.app",
    "https://mussarat123shamsher-physical-ai-book.hf.space",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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

# Tool schemas for the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for the latest information when the textbook is insufficient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_db",
            "description": "Save important notes or information to the database for later reference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {"type": "string", "description": "The content to save."}
                },
                "required": ["note"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email with specific information to a recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_email": {"type": "string", "description": "Recipient email address."},
                    "subject": {"type": "string", "description": "Email subject."},
                    "body": {"type": "string", "description": "The main content of the email."}
                },
                "required": ["to_email", "subject", "body"]
            }
        }
    }
]

# ---------------------------------
# ROUTES
# ---------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
async def agent_query(req: QueryRequest):
    """The main Agent loop that uses LLM Tool Calling."""
    
    # 1. Get initial context from the textbook
    book_data = get_book_context(req.question)
    
    messages = [
        {
            "role": "system", 
            "content": (
                "You are the 'Physical AI Assistant'. You help users understand humanoid robotics.\n"
                f"CURRENT TEXTBOOK CONTEXT:\n{book_data['context']}\n\n"
                "INSTRUCTIONS:\n"
                "1. Use the textbook context first. If it answers the question, respond directly.\n"
                "2. If the textbook is missing info, use 'web_search'.\n"
                "3. Use 'save_to_db' if the user wants to remember or save something.\n"
                "4. Use 'send_email' if the user wants to email information.\n"
                "5. Be professional and concise."
            )
        },
        {"role": "user", "content": req.question}
    ]

    try:
        # Initial call to see if LLM wants to use a tool
        response = await llm_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=1024
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            # Handle tool calls
            tool_used = "Multiple/None"
            final_answer = ""
            
            # Append the assistant's message with tool calls once
            messages.append(response_message)
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                tool_used = function_name
                
                logger.info(f"Agent decided to use tool: {function_name} with args: {args}")

                if function_name == "web_search":
                    result = web_search(args.get("query"))
                elif function_name == "save_to_db":
                    result = save_to_db("user_notes", {
                        "note": args.get("note"), 
                        "user": req.user_email or "anonymous"
                    })
                elif function_name == "send_email":
                    # Use provided email or fallback to user's registered email
                    recipient = args.get("to_email") or req.user_email
                    if not recipient:
                        result = "Error: No recipient email provided."
                    else:
                        result = send_email(recipient, args.get("subject"), args.get("body"))
                else:
                    result = "Error: Unknown tool."

                # Append tool result message
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                })

            # Final call to summarize tool results
            second_response = await llm_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            final_answer = second_response.choices[0].message.content
            
            return QueryResponse(
                answer=final_answer,
                sources=book_data['sources'] if "web" not in tool_used.lower() else [],
                tool_used=tool_used
            )
        
        else:
            # No tool call needed, return standard RAG response
            return QueryResponse(
                answer=response_message.content,
                sources=book_data['sources'],
                tool_used="Textbook"
            )

    except Exception as e:
        logger.error(f"Query error: {e}")
        return QueryResponse(
            answer=f"I encountered an error while processing your request: {str(e)}",
            sources=[],
            tool_used="Error"
        )

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), user_email: Optional[str] = Form(None)):
    """Dynamically upload, chunk, embed a new document and save metadata."""
    try:
        from qdrant_client.models import PointStruct
        import io
        
        content = await file.read()
        text = ""
        
        # 1. Extract text based on file type
        if file.filename.endswith(".pdf"):
            try:
                from pypdf import PdfReader
                pdf_file = io.BytesIO(content)
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            except ImportError:
                raise HTTPException(status_code=500, detail="PDF support (pypdf) not installed on server.")
        else:
            # Assume text/md
            text = content.decode("utf-8")
            
        if not text.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in file.")

        # 2. Chunk the text (using the logic from embed.py for consistency)
        def chunk_text(text, size=400, overlap=50):
            words = text.split()
            for i in range(0, len(words), size - overlap):
                yield " ".join(words[i:i + size])
        
        chunks = list(chunk_text(text))
        if not chunks:
            raise HTTPException(status_code=400, detail="File content too short to index.")

        # 3. Embed and Upsert chunks
        points = []
        for chunk in chunks:
            vector = embedding_model.encode(chunk).tolist()
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk, 
                    "source": file.filename, 
                    "user": user_email or "anonymous"
                }
            ))
        
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        # 4. Save metadata to Firestore
        save_to_db("uploaded_files", {
            "filename": file.filename,
            "user": user_email or "anonymous",
            "size": len(content),
            "type": file.content_type,
            "category": "Reference",
            "status": "Processed",
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        return {"status": "success", "message": f"Uploaded, chunked ({len(chunks)} parts), and indexed {file.filename}"}
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

