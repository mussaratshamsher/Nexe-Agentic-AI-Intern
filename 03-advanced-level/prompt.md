# backend
# ROLE

You are an expert Senior AI Systems Architect and Python backend engineer.

Your task is to build a production-ready backend for an advanced-level multi-agent SaaS application called:

# “AI Business Operations Manager”

The backend must use:

* FastAPI
* OpenAI Agents SDK
* PostgreSQL (Supabase)
* Async Python architecture
* Modular scalable structure
* Render deployment compatibility

This is NOT a beginner chatbot project.

This is a real-world autonomous multi-agent AI business system.

The backend must be designed carefully with clean architecture, scalability, observability, logging, and future extensibility in mind.

---

# PRIMARY OBJECTIVE

Build ONLY the backend system.

The backend should support:

* Multi-agent orchestration
* Autonomous workflows
* Task delegation
* CRM management
* Execution logs
* Multi-step reasoning
* Tool calling
* API integrations
* Persistent memory
* Real-time business operations

The system should look like a startup-grade SaaS backend.

---

# CORE APPLICATION IDEA

This platform acts like a team of AI employees for businesses.

Users interact through:

* Web frontend
* WhatsApp
* Email (future-ready)

The system intelligently:

* Handles customer support
* Qualifies leads
* Plans tasks
* Generates proposals
* Tracks execution logs
* Maintains CRM records
* Delegates tasks between agents

---

# REQUIRED TECH STACK

Use ONLY these technologies unless absolutely necessary:

## Backend Framework

* FastAPI

## AI Framework

* OpenAI Agents SDK

## Database

* PostgreSQL (Supabase)

## ORM / Database Toolkit

* SQLAlchemy (async)
* asyncpg

## Validation

* Pydantic v2

## Authentication

* JWT auth
* Supabase Auth compatible

## Deployment

* Render-compatible architecture

## Queue / Async Tasks

* BackgroundTasks initially
* Future-ready for Redis/Celery

## Environment

* Python 3.12+

---

# IMPORTANT ENGINEERING RULES

## 1. Use CLEAN ARCHITECTURE

The codebase must be:

* modular
* maintainable
* scalable
* production-ready

Avoid monolithic code.

---

## 2. EVERYTHING MUST BE ASYNC

Use:

* async routes
* async database
* async tools

---

## 3. USE TYPE SAFETY

Use:

* type hints everywhere
* Pydantic schemas
* structured outputs

---

## 4. NEVER HARD-CODE

Use:

* environment variables
* config management

---

## 5. ADD EXECUTION LOGGING

Every important action must generate logs.

Store:

* agent execution
* task delegation
* errors
* workflow actions
* timestamps

This is CRITICAL.

---

# REQUIRED PROJECT ARCHITECTURE

Generate a clean scalable folder structure.

Use something close to:

backend/
│
├── app/
│   ├── main.py
│   ├── config/
│   ├── api/
│   ├── agents/
│   ├── orchestration/
│   ├── services/
│   ├── tools/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── middleware/
│   ├── core/
│   ├── logs/
│   ├── utils/
│   └── integrations/
│
├── requirements.txt
├── render.yaml
├── .env.example
└── README.md

---

# REQUIRED DATABASE TABLES

Design PostgreSQL models for:

## 1. users

* id
* email
* hashed_password
* role
* created_at

## 2. customers

* id
* name
* email
* phone
* company
* created_at

## 3. conversations

* id
* customer_id
* channel
* status
* created_at

## 4. messages

* id
* conversation_id
* sender_type
* content
* timestamp

## 5. tickets

* id
* customer_id
* priority
* status
* assigned_agent
* created_at

## 6. execution_logs

* id
* agent_name
* action
* status
* details
* timestamp

## 7. tasks

* id
* task_type
* assigned_agent
* status
* result
* created_at

---

# REQUIRED MULTI-AGENT SYSTEM

Implement multiple specialized agents using OpenAI Agents SDK.

---

# AGENT 1 — MASTER ORCHESTRATOR AGENT

Responsibilities:

* Receive requests
* Analyze intent
* Plan workflow
* Delegate tasks
* Combine outputs
* Maintain execution chain

This is the brain of the system.

---

# AGENT 2 — SUPPORT AGENT

Responsibilities:

* Customer support
* FAQ handling
* Ticket generation
* Escalation detection

---

# AGENT 3 — SALES AGENT

Responsibilities:

* Lead qualification
* Service recommendation
* Budget analysis
* Inquiry classification

---

# AGENT 4 — PROJECT MANAGER AGENT

Responsibilities:

* Multi-step reasoning
* Project planning
* Timeline generation
* Task decomposition

---

# AGENT 5 — CONTENT AGENT

Responsibilities:

* Proposal generation
* Email drafting
* Communication formatting

---

# REQUIRED AGENT FEATURES

Every agent must support:

* tool calling
* structured outputs
* execution tracing
* logging
* memory access
* context awareness

---

# REQUIRED TOOL SYSTEM

Create production-ready tools.

Tools must include:

## CRM Tools

* create_customer
* get_customer_history
* create_ticket
* get_open_tickets

## Knowledge Tools

* search_knowledge_base

## Logging Tools

* log_execution_step

## Communication Tools

* send_email (mock initially)
* send_whatsapp_message (mock initially)

---

# REQUIRED API ROUTES

Create scalable API routes.

## Auth

* /auth/register
* /auth/login

## Chat

* /chat/message

## CRM

* /customers
* /tickets
* /conversations

## Logs

* /logs/executions

## Health

* /health

---

# REQUIRED EXECUTION FLOW

Implement this workflow:

1. User sends message
2. Backend receives request
3. Conversation stored
4. Orchestrator agent activated
5. Agent plans tasks
6. Delegates specialized agents
7. Tools are executed
8. Execution logs stored
9. Final response generated
10. Response saved
11. API returns response

---

# REQUIRED EXECUTION LOGGING

VERY IMPORTANT.

The system must generate detailed execution traces like:

[10:01] User request received
[10:02] Orchestrator activated
[10:03] Sales agent delegated
[10:04] Lead qualification complete
[10:05] PM agent generated roadmap
[10:06] Final response created

Store these in database.

---

# REQUIRED ERROR HANDLING

Implement:

* try/except patterns
* structured API errors
* logging
* validation handling

Never crash silently.

---

# REQUIRED SECURITY

Implement:

* JWT auth
* CORS
* environment variable protection
* input validation

---

# REQUIRED CONFIGURATION

Create:

* .env.example
* settings management
* modular config

Environment variables should include:

* OPENAI_API_KEY
* DATABASE_URL
* JWT_SECRET
* SUPABASE_URL
* SUPABASE_KEY

---

# REQUIRED RENDER DEPLOYMENT SUPPORT

The backend must be fully deployable on Render.

Generate:

* render.yaml
* startup command
* requirements.txt
* production settings

---

# REQUIRED README

Generate professional README containing:

* setup instructions
* environment variables
* deployment guide
* architecture explanation
* API overview

---

# IMPORTANT IMPLEMENTATION RULES

## DO NOT:

* create toy examples
* create fake architecture
* use simplistic code
* create everything in one file

---

## DO:

* create real scalable architecture
* separate concerns properly
* use production patterns
* use async architecture
* structure agents professionally

---

# OUTPUT EXPECTATION

Generate the backend step-by-step in proper order.

Start with:

1. project structure
2. dependencies
3. config
4. database
5. agents
6. orchestration
7. tools
8. APIs
9. deployment

Explain every major engineering decision while coding.

Do not skip architecture planning.
