from groq import AsyncGroq
from ...config.settings import settings
from ...logs.execution_logger import ExecutionLogger
import json

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class SupportAgent:
    def __init__(self):
        self.name = "Support Agent"
        self.instructions = """
        You are a Support Agent for a business operations platform.
        Your goal is to handle customer inquiries and solve technical issues.
        Use the provided 'Knowledge' context (RAG) to find answers and 'Customer Profile' to see their history.
        Be polite, professional, and helpful.
        If you cannot find an answer in the context, state that you will escalate it.
        """

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Processing support request", input_text[:50] + "...", repo)
        
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
        await ExecutionLogger.log(self.name, "Generated support response", f"Length: {len(result)}", repo)
        return result
