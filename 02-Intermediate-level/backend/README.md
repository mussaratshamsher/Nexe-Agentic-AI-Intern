# Physical AI Agent - Backend (Intermediate Level)

This is the FastAPI backend for the Physical AI Agent. it provides RAG (Retrieval-Augmented Generation) capabilities and a multi-tool agent system.

## 🚀 Features
- **RAG Assistant**: Contextual answers based on the Physical AI textbook.
- **Dynamic Ingestion**: Upload `.txt` or `.md` files to expand the agent's knowledge in real-time.
- **Multi-Tool Agent**:
  - 🌐 **Web Search**: Uses Tavily for real-time information.
  - 📂 **Database**: Saves user notes and file metadata to Firebase Firestore.
  - 📧 **Email**: Sends summaries and information via Resend.

## 🛠️ Setup

### 1. Prerequisites
- Python 3.10+
- [Groq API Key](https://console.groq.com/) (for Llama-3.1 LLM)
- [Qdrant Cloud Account](https://qdrant.tech/) (for Vector DB)
- [Tavily API Key](https://tavily.com/) (for Search)
- [Resend API Key](https://resend.com/) (for Email)
- [Firebase Service Account](https://console.firebase.google.com/) (for Firestore)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Environment Variables (.env)
Create a `.env` file in this directory:
```env
GROQ_API_KEY=your_groq_key
QDRANT_CLUSTER_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
TAVILY_API_KEY=your_tavily_key
RESEND_API_KEY=your_resend_key
# For Firebase, either place 'physical-ai-auth.json' in this folder 
# or set FIREBASE_SERVICE_ACCOUNT as a JSON string.
```

### 4. Ingesting the Textbook
Run the ingestion script to populate your Qdrant collection:
```bash
# Set the path to your book docs
export BOOK_CONTENT_PATH="../book/docs" 
python embed.py
```

### 5. Run the Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🐳 Docker (Optional)
Built for deployment on Hugging Face Spaces or other container platforms:
```bash
docker build -t physical-ai-backend .
docker run -p 7860:7860 physical-ai-backend
```
