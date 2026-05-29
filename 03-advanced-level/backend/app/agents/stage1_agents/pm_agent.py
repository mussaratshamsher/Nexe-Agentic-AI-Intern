from groq import AsyncGroq
from ...config.settings import settings
from ...logs.execution_logger import ExecutionLogger
import json

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class PMAgent:
    def __init__(self):
        self.name = "Project Manager Agent"
        self.instructions = """
        You are a Project Manager Agent. Your goal is task decomposition and timeline generation.
        Use the provided context to align your planning with existing project history or company guidelines.
        Provide clear, numbered implementation roadmaps with estimated timelines.
        """

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Planning workflow/roadmap", input_text[:50] + "...", repo)
        
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
        await ExecutionLogger.log(self.name, "Roadmap generated", None, repo)
        return result
