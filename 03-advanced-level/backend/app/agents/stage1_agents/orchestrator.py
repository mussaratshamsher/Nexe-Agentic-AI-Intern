import json
from groq import AsyncGroq
from ...config.settings import settings
from ...logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class OrchestratorAgent:
    def __init__(self):
        self.name = "Mussarat Shamsher"
        self.instructions = """
        You are the Master Orchestrator of an AI Business Operations system.
        You are an autonomous employee, wise, thoughtful, and professional.

        CORE CAPABILITIES:
        1. Contextual Awareness: Use the provided "Knowledge" and "Customer Profile" to tailor your plan.
        2. Sensitivity & Uncertainty: If a task involves legal agreements, financial disputes, high-stakes decisions, or you are fundamentally uncertain, mark "is_sensitive": true, explain your reasoning in "review_reason", and instruct that the task must be escalated to admin for manual review.
        3. Human-like Wisdom: For professional requests, act grateful, thoughtful, and articulate.

        CHANNELS & STYLE:
        - Email: Formal, detailed, include greeting/signature.
        - WhatsApp: Concise, conversational, under 300 chars.
        - Web Form: Semi-formal, helpful, structured.

        WORKFLOW:
        1. Analyze intent and sensitivity using the provided Context.
        2. Plan tasks for specialized agents (Sales, Support, PM, Content).
        3. Output the plan in JSON format.
        
        JSON STRUCTURE MANDATE:
        {
            "plan": [
                {"agent": "Sales", "task": "qualify the lead and analyze budget", "reasoning": "...", "step_number": 1},
                {"agent": "PM", "task": "create a rollout plan", "reasoning": "...", "step_number": 2}
            ],
            "is_sensitive": false,
            "strategic_reasoning": "...",
            "channel_guidelines": "..."
        }
        """

    async def analyze_and_plan(self, user_request: str, channel: str = "web", repo=None, history: str = "", context: dict = None):
        await ExecutionLogger.log(self.name, f"Analyzing request from {channel}", user_request[:50] + "...", repo)
        
        context_str = json.dumps(context, indent=2) if context else "No extra context."
        prompt = f"History: {history}\n\nEnriched Context:\n{context_str}\n\nChannel: {channel}\nRequest: {user_request}"
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        plan_data = json.loads(response.choices[0].message.content)
        await ExecutionLogger.log(self.name, "Workflow plan finalized", f"{len(plan_data.get('plan', []))} steps. Sensitive: {plan_data.get('is_sensitive')}", repo)
        return plan_data

    async def synthesize(self, original_request: str, agent_outputs: list, channel: str, guidelines: str, repo=None, history: str = ""):
        await ExecutionLogger.log(self.name, "Synthesizing final response (streaming)", f"Channel: {channel}", repo)
        
        context = "\n".join([f"Agent {o['agent']}: {o['output']}" for o in agent_outputs])
        
        system_prompt = f"""
        You are the Master Orchestrator, a highly professional AI assistant. 
        Synthesize the agent outputs into a final response.

        CRITICAL QUALITY STANDARDS:
        1. PERSONALIZATION: Use the agent outputs and context to be highly specific.
        2. TONE: Maintain a high level of professional wisdom, warmth, and genuine gratitude. 
        3. CHANNEL RULES: 
           - Channel: {channel}
           - Guidelines: {guidelines}
        """
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original Request: {original_request}\n\nAgent Context:\n{context}"}
            ],
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
