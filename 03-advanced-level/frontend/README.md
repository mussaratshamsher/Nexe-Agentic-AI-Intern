# AI Business Operations Manager (Phase 3)

## Project Overview
The AI Business Operations Manager is an advanced, multi-agent SaaS platform designed to automate complex business workflows. By integrating specialized AI agents (Sales, Content, Support, PM) with a robust CRM backend, it transforms manual, time-consuming business processes into autonomous, high-efficiency operations. This platform bridges the gap between raw AI models and enterprise-grade business utility.

## Tech Stack
*   **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui, Zustand (State Management).
*   **Backend:** FastAPI (Python), SQLAlchemy (ORM), PostgreSQL/SQLite, Integrated AI Agent orchestration.
*   **Infrastructure & Tools:** Docker, JWT Authentication, Supabase, Vercel for deployment.

## LLM Strategy: Free vs. Paid
*   **Free LLMs:** Ideal for prototyping, low-complexity tasks, and environments requiring strict data privacy (on-prem).
*   **Paid LLMs (e.g., GPT-4o, Claude 3.5 Sonnet):** Essential for high-reasoning, complex multi-step workflows, creative content generation, and high-volume production tasks where accuracy is paramount. Our architecture supports dynamic switching based on task complexity.

## Human vs. AI Efficiency: Token Comparison
*   **Throughput:** A single AI agent processes thousands of tokens—equivalent to hours of human research—in seconds.
*   **Consistency:** Unlike human operators, AI agents maintain 100% operational consistency 24/7, eliminating cognitive fatigue and human error in repetitive tasks.
*   **Cost-Effectiveness:** When accounting for time-to-value, the cost per token is orders of magnitude lower than equivalent human labor.
*   **Token Usage & Cost Estimates (per Request):**
    *   **Simple Query (e.g., Status check):** ~500 tokens | ~$0.001
    *   **Agentic Task (e.g., Content draft):** ~2,500 tokens | ~$0.01
    *   **Complex Workflow (e.g., CRM analysis):** ~10,000+ tokens | ~$0.05+
    *   *Note: Costs are estimates based on standard GPT-4o-mini pricing and may vary based on model selection and input complexity.*

## Backend Features
*   **Multi-Agent Orchestration:** Specialized agents (Sales, PM, Content, Support) working in concert.
*   **Intelligent CRM:** Automated data ingestion, prospect management, and historical tracking.
*   **Workflow Engine:** Execution logging, error handling, and state management for long-running processes.
*   **Secure API Layer:** Robust authentication and role-based access control.

## Frontend Features
*   **Real-time Dashboard:** Operational overview and KPIs.
*   **Unified Chat Interface:** Interact with multiple agents in a single workspace.
*   **CRM Data Visualization:** Visual representation of customer interactions and pipeline status.
*   **Execution Logs:** Transparent monitoring of agent activities and decisions.

## Capabilities & Power
*   **What it does:** Automates prospect outreach, content generation, support ticket resolution, and project management updates.
*   **Why it's powerful:** It turns business logic into executable code. It doesn't just "talk"; it *acts* on behalf of the business.
*   **Professional Value:** As a professional solution, it offers scalability, auditability, and massive reduction in overhead. It is a force multiplier for any team, allowing human professionals to focus on strategy rather than execution.
*   **Core Strength:** The combination of *specialized agents* (depth) and *workflow orchestration* (breadth) creates a system that is greater than the sum of its parts.

## Getting Started

### Prerequisites
- Node.js 18+
- npm

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy `.env.local.example` to `.env.local` and configure your variables:
   ```bash
   cp .env.local.example .env.local
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```

## Folder Structure
- `app/`: Next.js pages and layouts
- `components/`: Reusable UI components
- `lib/`: Utilities, API clients, hooks, stores, validations
- `services/`: Service layer for API interaction
- `types/`: TypeScript definitions

## API Integration
The frontend communicates with the FastAPI backend via `src/lib/api/client.ts`. All service calls are centralized in the `services/` directory.

## Deployment
This project is configured for deployment on Vercel.

calculator: https://ai-agent-and-calculate.streamlit.app/
