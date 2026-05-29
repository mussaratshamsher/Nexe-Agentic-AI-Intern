from groq import AsyncGroq
from ...config.settings import settings
from ...tools.communication_tools import CommunicationTools
from ...logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class ContentAgent:
    def __init__(self):
        self.name = "Content Agent"
        self.instructions = """
        You are a Content Agent. Your goal is to draft professional emails, proposals, and business communications.
        
        SPECIAL ABILITY: ONE-CLICK MARKETING PACKS
        If requested to create a 'marketing pack' or 'project content', generate:
        1. A professional announcement email.
        2. A LinkedIn/Social media post.
        3. A brief project summary for internal use.
        
        Ensure a professional tone and clear structure.
        Use communication tools to send messages when requested.
        """

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Drafting content", input_text[:50] + "...", repo)
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        await ExecutionLogger.log(self.name, "Draft complete", None, repo)
        return result
