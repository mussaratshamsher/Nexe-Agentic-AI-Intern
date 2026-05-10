# Physical AI & Humanoid Robotics - Interactive Book

This is a modern, interactive textbook built with [Docusaurus](https://docusaurus.io/). It covers the principles, technologies, and practices of building intelligent humanoid robots.

## 🤖 AI Agent Features
This book includes an integrated **Physical AI Agent** (Chatbot) that allows readers to:
- **Ask Questions**: Get contextual answers directly from the textbook chapters.
- **Search the Web**: Access the latest research and news beyond the book's content.
- **Save Notes**: Persist important insights directly to a personal database (Firebase).
- **Email Info**: Send chapter summaries or AI answers to your inbox.
- **Upload Knowledge**: Dynamically add your own notes or research papers to the agent's memory.

## 🛠️ Tech Stack
- **Frontend**: React, Docusaurus, TypeScript, Firebase Auth.
- **Backend**: FastAPI (Python), Llama-3.1 (via Groq), Qdrant Vector DB.
- **Tools**: Tavily (Search), Resend (Email), Firestore (DB).

## 🚀 Getting Started

### 1. Installation
```bash
npm install
```

### 2. Environment Setup
Create a `.env` file based on the provided configuration for Backend URL and Firebase keys.

### 3. Local Development
```bash
npm start
```

### 4. Build for Production
```bash
npm run build
```

## 🌐 Deployment
The frontend is optimized for [Vercel](https://vercel.com/). Ensure all environment variables are configured in the Vercel project settings.
