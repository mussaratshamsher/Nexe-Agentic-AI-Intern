---
title: AI Business Operations Manager
emoji: 💼
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI Business Operations Manager - Phase 4 Backend

## Overview
Phase 4 of the AI Business Operations Manager extends the production-ready FastAPI backend with multi-channel communication capabilities and advanced automation. It features persistent storage, secure JWT authentication, and integrated tools for Gmail and WhatsApp (Evolution API).

## Architecture
- **FastAPI**: Asynchronous REST API framework.
- **PostgreSQL**: Primary database.
- **SQLAlchemy Async**: ORM for database abstraction.
- **Pydantic v2**: Data validation.
- **JWT**: Secure token-based authentication.
- **Google OAuth**: For Gmail integration.

## Project Structure
```
phase-04/
├── app/
│   ├── api/                    # REST API routes (Auth, Chat, CRM, Logs, Webhooks)
│   ├── core/                   # Security, JWT, and shared dependencies
│   ├── db/                     # Database models and session management
│   ├── repositories/           # Data access layer (CRUD operations)
│   ├── services/               # Business logic layer
│   ├── schemas/                # Pydantic validation models
│   ├── orchestration/          # Multi-agent workflow logic
│   ├── agents/                 # AI Agent definitions
│   └── tools/                  # Agent tools (CRM, Knowledge Base, Gmail, WhatsApp)
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
├── credentials.json            # Google API credentials
└── init_db.py                  # Database initialization script
```

## Setup & Installation

1. **Environment**: Ensure Python 3.12+ is installed.
2. **Dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
3. **Database**: Configure your `.env` with the appropriate `DATABASE_URL` (using `postgresql+asyncpg` for async support).
4. **Database Initialization**:
   ```bash
   python init_db.py
   ```
5. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Hugging Face Deployment

To deploy this API on Hugging Face Spaces:

1. **Create a New Space**: Choose "Docker" as the SDK.
2. **Upload Files**: Upload all files from the `phase-04` directory (excluding sensitive files like `.env`, `credentials.json`, and `token.json`).
3. **Configure Secrets**: In your Space settings, add the following variables as **Secrets**:
   - `GROQ_API_KEY`
   - `DATABASE_URL` (e.g., your Supabase or Neon PostgreSQL URL)
   - `JWT_SECRET`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - Any other variables listed in `app/config/settings.py`
4. **Google API Credentials**: For Gmail integration, you will need to handle `credentials.json` and `token.json`. It is recommended to mount these as persistent storage or encode them into environment variables if they are small enough, though the current implementation expects them as local files.

## Key API Endpoints
- **POST /api/v1/auth/register**: User registration
- **POST /api/v1/auth/login**: JWT Authentication
- **POST /api/v1/chat/message**: Main AI interaction endpoint
- **GET /api/v1/customers**: CRM Lead management
- **GET /api/v1/tickets**: Support ticket management
- **GET /api/v1/logs**: Real-time execution logs for agents

## Features
- **Multi-Agent Orchestration**: Integrated backend logic for Sales, PM, and Support agents.
- **Real-time Logging**: Captures agent "thoughts" and actions for transparency.
- **Secure Auth**: JWT-based authentication for all protected routes.
- **Persistent Memory**: Session history and CRM data stored in PostgreSQL.
