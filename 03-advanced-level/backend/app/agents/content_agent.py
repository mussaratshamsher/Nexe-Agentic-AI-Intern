from typing import Dict, Any, List
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import Field
import json

from app.agents.base_agent import BaseAgent
from app.tools.tool_manager import ToolManager
from app.services.execution_log_service import ExecutionLogService
from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Mock tools for Content Agent
@tool(args_schema=None)
def generate_proposal(customer_needs: str, proposed_services: str) -> Dict[str, Any]:
    """
    Generates a professional proposal document based on customer needs and proposed services.
    """
    logger.info(f"Mock: Generating proposal for needs: {customer_needs}")
    return {"proposal_document": f"Proposal for {customer_needs}. Includes: {proposed_services}.", "status": "generated"}

@tool(args_schema=None)
def draft_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Drafts an email for a given recipient, subject, and body.
    This tool might call the send_email tool or just draft it.
    """
    logger.info(f"Mock: Drafting email to {recipient} - Subject: {subject}")
    return {"drafted_email": {"to": recipient, "subject": subject, "body": body}, "status": "drafted"}

class ContentAgent(BaseAgent):
    name: str = "Content Agent"
    description: str = "Generates proposals, drafts emails, and formats communications."
    llm: BaseChatModel
    tools: List[tool]
    tool_manager: ToolManager
    execution_log_service: ExecutionLogService

    def __init__(self,
                 llm: BaseChatModel,
                 tool_manager: ToolManager,
                 execution_log_service: ExecutionLogService,
                 ):
        agent_tools = [
            generate_proposal,
            draft_email,
            # It could also use the `send_email` tool directly if it's part of its scope
        ]
        super().__init__(name=self.name, description=self.description, llm=llm, tools=agent_tools)
        self.tool_manager = tool_manager
        self.execution_log_service = execution_log_service

    async def run(self, human_input: str, chat_history: List[BaseMessage] | None = None, **kwargs) -> Dict[str, Any]:
        """
        Handles content generation tasks like proposals and email drafts.
        """
        await self._log_execution("started", {"input": human_input})
        
        try:
            all_available_tools = self.tools + self.tool_manager.get_all_tools()
            
            content_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are the Content Agent. Your role is to generate professional content such as proposals and email drafts.
                You have access to tools for generating proposals and drafting emails.
                When a user requests content generation:
                1. Identify the type of content needed (proposal, email, etc.).
                2. Use the appropriate tool (`generate_proposal` or `draft_email`) with the necessary parameters.
                3. Log all significant actions using `log_execution_step`.
                4. Provide the generated content clearly to the user.
                """),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}")
            ])
            
            agent = create_openai_tools_agent(
                llm=self.llm,
                tools=all_available_tools,
                prompt=content_prompt
            )
            
            message_history = ChatMessageHistory(messages=chat_history if chat_history else [])
            agent_executor_instance = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=all_available_tools,
                verbose=settings.debug,
                handle_parsing_errors=True
            )

            agent_response = await agent_executor_instance.invoke(
                 {"input": human_input, "chat_history": chat_history if chat_history else []}
            )
            
            final_response_content = agent_response.get("output", "Content agent did not produce a final output.")
            await self._log_execution("completed", {"output": final_response_content, "agent_response_details": json.dumps(agent_response)})
            
            return {"output": final_response_content}

        except Exception as e:
            await self._log_execution("failed", {"error": str(e), "details": json.dumps(getattr(e, 'response', {}))})
            logger.error(f"Content Agent failed: {e}", exc_info=True)
            raise InternalServerErrorException(detail=f"Content Agent failed: {e}") from e
