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

# Mock tools for Support Agent
@tool(args_schema=None)
def create_support_ticket(customer_id: int, subject: str, description: str, priority: str="medium", assigned_agent_id: Optional[int]=None) -> Dict[str, Any]:
    """
    Creates a new support ticket for a customer.
    Use this when a customer reports an issue that requires support.
    """
    logger.info(f"Mock: Creating support ticket for customer {customer_id} - Subject: {subject}")
    # This tool definition is a bit redundant with crm_tools.create_ticket,
    # but it's useful for the agent to 'know' about its specific tasks.
    # In a real scenario, you might call the actual service directly or use a shared tool.
    return {"ticket_id": 101, "customer_id": customer_id, "subject": subject, "description": description, "priority": priority, "status": "open", "assigned_agent_id": assigned_agent_id}

@tool(args_schema=None)
def get_customer_support_history(customer_id: int) -> Dict[str, Any]:
    """
    Retrieves the support ticket history for a specific customer.
    """
    logger.info(f"Mock: Getting support history for customer ID: {customer_id}")
    return {"customer_id": customer_id, "tickets": [{"id": 101, "subject": "Issue with order", "status": "open"}]}

class SupportAgent(BaseAgent):
    name: str = "Support Agent"
    description: str = "Handles customer support inquiries, FAQ retrieval, and ticket creation."
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
            create_support_ticket,
            get_customer_support_history,
            # Can also use globally registered tools like search_knowledge_base
        ]
        super().__init__(name=self.name, description=self.description, llm=llm, tools=agent_tools)
        self.tool_manager = tool_manager
        self.execution_log_service = execution_log_service

    async def run(self, human_input: str, chat_history: List[BaseMessage] | None = None, **kwargs) -> Dict[str, Any]:
        """
        Handles support-related inquiries by creating tickets or retrieving history.
        """
        await self._log_execution("started", {"input": human_input})
        
        try:
            all_available_tools = self.tools + self.tool_manager.get_all_tools()
            
            support_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are the Support Agent. Your role is to assist customers with their inquiries,
                create support tickets when necessary, and retrieve their support history.
                You have access to tools for creating tickets, getting customer history, and searching knowledge.
                When a user expresses a support issue:
                1. Determine if a ticket needs to be created or if history retrieval is needed.
                2. Use `create_support_ticket` to log new issues, ensuring all details are captured.
                3. Use `get_customer_support_history` to understand past issues.
                4. Log all significant actions using `log_execution_step`.
                5. Respond to the user clearly and informatively.
                """),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}")
            ])
            
            agent = create_openai_tools_agent(
                llm=self.llm,
                tools=all_available_tools,
                prompt=support_prompt
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
            
            final_response_content = agent_response.get("output", "Support agent did not produce a final output.")
            await self._log_execution("completed", {"output": final_response_content, "agent_response_details": json.dumps(agent_response)})
            
            return {"output": final_response_content}

        except Exception as e:
            await self._log_execution("failed", {"error": str(e), "details": json.dumps(getattr(e, 'response', {}))})
            logger.error(f"Support Agent failed: {e}", exc_info=True)
            raise InternalServerErrorException(detail=f"Support Agent failed: {e}") from e
