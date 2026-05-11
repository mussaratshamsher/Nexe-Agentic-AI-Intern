# Physical AI & Humanoid Robotics Application Overview

An interactive, AI-powered textbook and research platform for humanoid robotics, featuring a Retrieval-Augmented Generation (RAG) agent that can search the book, the web, and manage user notes.

## 🚀 Tech Stack

### Frontend
- **Framework:** [Docusaurus](https://docusaurus.io/) (React + TypeScript)
- **Authentication:** [Firebase Auth](https://firebase.google.com/docs/auth)
- **Styling:** Custom Vanilla CSS & CSS Modules
- **Deployment:** [Vercel](https://vercel.com/)
- **Live URL:** [humanoid-robotics-book-sepia.vercel.app](https://humanoid-robotics-book-sepia.vercel.app/)

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **AI Models:** 
  - LLM: `Llama-3.1-8b-instant` via Groq
  - Embeddings: `all-MiniLM-L6-v2` (SentenceTransformers)
- **Vector Database:** [Qdrant](https://qdrant.tech/) (Cloud)
- **Database/Storage:** [Cloud Firestore](https://firebase.google.com/docs/firestore)
- **Deployment:** [Hugging Face Spaces](https://huggingface.co/spaces)
- **API URL:** [mussarat123shamsher-physical-ai-book.hf.space](https://mussarat123shamsher-physical-ai-book.hf.space/docs)

## ✨ Core Features

### 1. Interactive AI Agent (Chatbot)
- **RAG System:** Answers questions based on the textbook content with source attribution.
- **Multi-Tool Capabilities:**
  - **Web Search:** Fetches real-time information when textbook data is insufficient.
  - **Note Taking:** Saves important technical notes directly to the user's database.
  - **Email Integration:** Sends technical summaries or notes directly to the user's email.

### 2. Document Management
- **Dynamic Ingestion:** Users can upload **PDFs**, text files (.txt), or markdown files (.md) to be indexed in the vector store.
- **Smart Chunking:** Documents are automatically split into manageable parts for precise AI retrieval.
- **File Tracking:** Persistent metadata storage in Firestore for tracking uploaded resources.

### 3. Multilingual Support
- Fully localized interface in **English** and **Urdu**.
- Language switcher integration for global accessibility.

### 4. User Experience
- **Secure Auth:** Firebase-powered login and registration.
- **Responsive Design:** Optimized for Desktop, Tablet, and Mobile devices.
- **Dark Mode:** Support for system-preferred and manual color modes.

## 🛠 Deployment & Connectivity
- **Frontend-Backend Sync:** Secured via custom CORS configurations allowing seamless communication between Vercel and Hugging Face.
- **Environment Driven:** Configuration managed through environment variables for secure API key handling (Groq, Qdrant, Firebase).
