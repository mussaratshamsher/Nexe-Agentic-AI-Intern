from groq import AsyncGroq
from ...config.settings import settings
from ...logs.execution_logger import ExecutionLogger
import json

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class SalesAgent:
    def __init__(self):
        self.name = "Sales Agent"
        self.instructions = """
        You are a Sales Agent. Your goal is to qualify leads, analyze budgets, and recommend services.
        Use the provided 'Customer Profile' and 'Knowledge' context to provide highly personalized advice.
        Focus on value proposition and identifying business needs based on their industry and history.
        Always provide a structured lead qualification report.
        """

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Analyzing lead/opportunity", input_text[:50] + "...", repo)
        
        context_str = json.dumps(context, indent=2) if context else "No extra context."
        prompt = f"Context:\n{context_str}\n\nTask: {input_text}"
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content
        await ExecutionLogger.log(self.name, "Lead analysis complete", None, repo)
        return result
