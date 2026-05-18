# AI Business Operations Manager Backend

This backend system powers the "AI Business Operations Manager" SaaS application, leveraging FastAPI, OpenAI Agents SDK, and PostgreSQL (Supabase) to provide intelligent, multi-agent automation for businesses.

## Table of Contents

- [About the Project](#about-the-project)
- [Core Application Idea](#core-application-idea)
- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Deployment Guide](#deployment-guide)
  - [Render Deployment](#render-deployment)
- [API Overview](#api-overview)
- [Contributing](#contributing)
- [License](#license)

## About the Project

The "AI Business Operations Manager" backend is designed to act as a team of AI employees for businesses. It handles tasks such as customer support, lead qualification, task planning, proposal generation, CRM management, and execution logging, all driven by a multi-agent system.

## Core Application Idea

This platform intelligently:
*   Handles customer support.
*   Qualifies leads.
*   Plans tasks.
*   Generates proposals.
*   Tracks execution logs.
*   Maintains CRM records.
*   Delegates tasks between agents.

Users interact with the system via a web frontend, WhatsApp, or email (future-ready).

## Tech Stack

-   **Backend Framework**: FastAPI
-   **AI Framework**: OpenAI Agents SDK (integrated with Langchain)
-   **Database**: PostgreSQL (Supabase)
-   **ORM / Database Toolkit**: SQLAlchemy (async), asyncpg
-   **Validation**: Pydantic v2
-   **Authentication**: JWT auth, Supabase Auth compatible
-   **Deployment**: Render-compatible architecture
-   **Queue / Async Tasks**: BackgroundTasks initially (future-ready for Redis/Celery)
-   **Environment**: Python 3.12+

## Architecture Overview

The backend follows a Clean Architecture principles, ensuring modularity, maintainability, scalability, and production-readiness. Key components include:

-   **API Layer**: Handles incoming requests, routes them, and returns responses.
-   **Orchestration Layer**: Manages the flow of requests, delegates tasks to agents, and synthesizes results.
-   **Agents Layer**: Contains specialized AI agents (Master Orchestrator, Sales, Support, etc.) responsible for specific tasks.
-   **Tools Layer**: Provides functional tools that agents can call (CRM, communication, logging, etc.).
-   **Services Layer**: Contains business logic that agents or controllers can use (e.g., customer management).
-   **Database Layer**: Manages data persistence using SQLAlchemy ORM with PostgreSQL.
-   **Core Layer**: Houses common utilities, security functions, exceptions, and configuration.
-   **Integrations**: Handles external service connections (e.g., Supabase).

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization
│   ├── config/                # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py        # Pydantic settings
│   │   └── config.py          # Other config-related utilities
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── v1/                # API versioning
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── crm.py
│   │   │   ├── logs.py
│   │   │   ├── health.py
│   │   │   └── endpoints.py   # For route aggregation
│   │   └── deps.py            # Dependency injection utilities
│   ├── agents/                # Agent definitions and logic
│   │   ├── __init__.py
│   │   ├── base_agent.py      # Base agent class
│   │   ├── master_orchestrator.py
│   │   ├── sales_agent.py
│   │   ├── support_agent.py
│   │   ├── project_manager_agent.py
│   │   ├── content_agent.py
│   │   └── utils.py           # Agent-specific utilities
│   ├── orchestration/         # Orchestration logic and workflows
│   │   ├── __init__.py
│   │   ├── orchestrator.py    # Core orchestration engine
│   │   └── workflows/         # Predefined workflows
│   │       └── __init__.py
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── execution_log_service.py # Placeholder for actual logging service
│   │   └── ...                # Other services like customer, ticket, etc.
│   ├── tools/                 # Agent tools
│   │   ├── __init__.py
│   │   ├── base_tool.py       # Base tool class
│   │   ├── crm_tools.py
│   │   ├── knowledge_tools.py
│   │   ├── logging_tools.py
│   │   ├── communication_tools.py
│   │   └── tool_manager.py    # Tool registration/lookup
│   ├── db/                    # Database connection and session management
│   │   ├── __init__.py
│   │   ├── database.py        # DB connection setup
│   │   ├── session.py         # Async session handling
│   │   └── repositories/      # Data access objects (optional, but good for separation)
│   │       ├── __init__.py
│   │       ├── base_repository.py
│   │       └── ...            # Repos for User, Customer, Ticket, etc.
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py            # Base model
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── ticket.py
│   │   ├── execution_log.py
│   │   └── task.py
│   ├── schemas/               # Pydantic models for API validation and data transfer
│   │   ├── __init__.py
│   │   ├── base.py            # Base schema
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── crm.py
│   │   ├── logs.py
│   │   └── agent.py           # Schemas related to agents/tasks
│   ├── middleware/            # Custom FastAPI middleware
│   │   ├── __init__.py
│   │   └── auth_middleware.py # JWT auth middleware
│   ├── core/                  # Core application components (e.g., auth, exceptions)
│   │   ├── __init__.py
│   │   ├── exceptions.py      # Custom API exceptions
│   │   ├── security.py        # JWT handling, password hashing
│   │   └── constants.py       # Application constants
│   ├── logs/                  # Logging configuration
│   │   ├── __init__.py
│   │   └── logger.py          # Logging setup
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── datetime_utils.py
│   │   ├── security_utils.py
│   │   └── etc...
│   └── integrations/          # External service integrations
│       ├── __init__.py
│       └── supabase.py        # Supabase client setup
│
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   └── ...
│
├── .env.example
├── requirements.txt
├── render.yaml
├── README.md
└── pyproject.toml             # For Python project configuration (optional, but good practice)
```

## Getting Started

### Prerequisites

-   Python 3.12+
-   Poetry (optional, for dependency management if preferred over pip)
-   Docker (for running Supabase locally, if needed)
-   An OpenAI API Key
-   Supabase project (URL and keys)

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>/backend
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Copy the `.env.example` file to `.env` and fill in your credentials:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file with your actual `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `JWT_SECRET`, and `DATABASE_URL`. Ensure these are correct for your local Supabase instance or remote project.

### Environment Variables

The following environment variables are required (refer to `.env.example` for details):

-   `OPENAI_API_KEY`: Your OpenAI API key.
-   `SUPABASE_URL`: The URL of your Supabase project.
-   `SUPABASE_KEY`: The Supabase Anon public key.
-   `SUPABASE_SERVICE_ROLE_KEY`: The Supabase Service Role key for backend access.
-   `DATABASE_URL`: The connection string for your PostgreSQL database (e.g., Supabase).
-   `JWT_SECRET`: A strong secret key for signing JWT tokens.
-   `SECRET_KEY`: A secret key for FastAPI (e.g., for session management if used).
-   `DEBUG`: Set to `True` for development, `False` for production.
-   `LOG_LEVEL`: Logging level (e.g., `INFO`, `DEBUG`).

## Running the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload --port 8000
```

The application will be accessible at `http://127.0.0.1:8000`. API documentation will be available at `http://127.0.0.1:8000/api/v1/docs`.

## Deployment Guide

### Render Deployment

1.  **Create a Render account** and a new Web Service.
2.  **Connect your Git repository.**
3.  **Configure Build Command**: `pip install --no-cache-dir -r requirements.txt`
4.  **Configure Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  **Set Environment Variables**:
    -   For sensitive variables like `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `JWT_SECRET`, `SECRET_KEY`, and `DATABASE_URL`, use Render's "Secrets" feature. Create these secrets in Render and link them to the corresponding environment variables in your service settings.
    -   Set `DEBUG` to `False`.
    -   Set `LOG_LEVEL` to `INFO` or `WARNING` for production.
6.  **Health Check**: Configure the health check to point to `/api/v1/health`.
7.  **Automatic Deployment**: Configure auto-deploy from your main branch.

The `render.yaml` file in the root of the `backend` directory provides a template for Render configuration.

## API Overview

The backend exposes a RESTful API with versioning (`/api/v1`). Key endpoints include:

-   **Health Check**: `/api/v1/health`
-   **Authentication**: `/api/v1/auth/register`, `/api/v1/auth/login`
-   **Chat**: `/api/v1/chat/message`
-   **CRM**: `/api/v1/customers`, `/api/v1/tickets`
-   **Logs**: `/api/v1/logs/executions`

Refer to the interactive API documentation at `/api/v1/docs` for detailed endpoints and request/response schemas.

## Contributing

Contributions are welcome! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure they are well-tested.
4.  Commit your changes with clear messages.
5.  Submit a Pull Request.

## License

[MIT License] (LICENSE file not yet created)
