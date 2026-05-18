from typing import Dict, Any, List
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import Field
import json

from app.agents.base_agent import BaseAgent
from app.tools.tool_manager import ToolManager # To access other tools/agents
from app.services.execution_log_service import ExecutionLogService
from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Mock tools for Sales Agent
@tool(args_schema=None)
def qualify_lead(lead_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Qualifies a lead based on provided information.
    Returns a qualification score and a recommendation (e.g., 'hot', 'warm', 'cold').
    """
    logger.info(f"Mock: Qualifying lead: {lead_info}")
    # Simulate qualification logic
    score = 0
    if lead_info.get("budget") and lead_info["budget"] > 5000:
        score += 1
    if lead_info.get("interest") and "enterprise" in lead_info["interest"].lower():
        score += 1
    if score >= 1:
        return {"qualification": "qualified", "score": score, "recommendation": "hot lead"}
    else:
        return {"qualification": "not qualified", "score": score, "recommendation": "cold lead"}

@tool(args_schema=None)
def recommend_service(lead_qualification: str, budget: Optional[float] = None) -> Dict[str, Any]:
    """
    Recommends a service package based on lead qualification and budget.
    """
    logger.info(f"Mock: Recommending service based on qualification: {lead_qualification}, budget: {budget}")
    if lead_qualification == "hot lead":
        if budget and budget > 10000:
            return {"service": "Enterprise Solution Package", "price": "$15,000"}
        else:
            return {"service": "Pro Business Package", "price": "$7,500"}
    else:
        return {"service": "Starter Package", "price": "$2,500", "note": "Follow up for more details"}

class SalesAgent(BaseAgent):
    name: str = "Sales Agent"
    description: str = "Specializes in lead qualification, service recommendation, and initial sales inquiries."
    llm: BaseChatModel
    tools: List[tool]
    tool_manager: ToolManager
    execution_log_service: ExecutionLogService
    
    def __init__(self,
                 llm: BaseChatModel,
                 tool_manager: ToolManager,
                 execution_log_service: ExecutionLogService,
                 ):
        # Sales agent's specific tools
        agent_tools = [
            qualify_lead,
            recommend_service,
            # It might also use tools registered in tool_manager like search_knowledge_base
        ]
        super().__init__(name=self.name, description=self.description, llm=llm, tools=agent_tools)
        self.tool_manager = tool_manager
        self.execution_log_service = execution_log_service

    async def run(self, human_input: str, chat_history: List[BaseMessage] | None = None, **kwargs) -> Dict[str, Any]:
        """
        Handles sales-related inquiries by qualifying leads and recommending services.
        """
        await self._log_execution("started", {"input": human_input})
        
        try:
            # Combine tools: Agent's own tools + globally available tools from tool_manager
            all_available_tools = self.tools + self.tool_manager.get_all_tools()
            
            # Prompt for the sales agent
            # This prompt guides the agent to qualify leads and recommend services.
            sales_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are the Sales Agent. Your goal is to qualify leads and recommend appropriate services.
                You have access to tools for lead qualification and service recommendation.
                When a user asks about services or provides lead information:
                1. Analyze the input to extract relevant details for lead qualification (e.g., budget, interest, company size).
                2. Use the `qualify_lead` tool to assess the lead's potential.
                3. Based on the qualification result, use `recommend_service` to suggest a suitable package.
                4. If specific information is missing, ask clarifying questions.
                5. Log all significant actions using the `log_execution_step` tool.
                6. Provide a clear, concise response to the user.
                """),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}")
            ])
            
            # Create the agent
            agent = create_openai_tools_agent(
                llm=self.llm,
                tools=all_available_tools,
                prompt=sales_prompt
            )
            
            # Use AgentExecutor to run the agent
            # Need to manage chat history properly. For simplicity, we pass it directly.
            # A full implementation might involve a memory object.
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
            
            final_response_content = agent_response.get("output", "Sales agent did not produce a final output.")
            await self._log_execution("completed", {"output": final_response_content, "agent_response_details": json.dumps(agent_response)})
            
            return {"output": final_response_content}

        except Exception as e:
            await self._log_execution("failed", {"error": str(e), "details": json.dumps(getattr(e, 'response', {}))})
            logger.error(f"Sales Agent failed: {e}", exc_info=True)
            raise InternalServerErrorException(detail=f"Sales Agent failed: {e}") from e
