import json
from typing import Dict, Any, List, Optional

from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.messages import BaseMessage

from app.config.settings import settings
from app.agents.master_orchestrator import MasterOrchestratorAgent # Our main orchestrator
from app.agents.base_agent import BaseAgent # For type hinting
from app.tools.tool_manager import ToolManager # To get tools and agent descriptions
from app.services.execution_log_service import ExecutionLogService # For logging
from app.logs.logger import setup_logger

logger = setup_logger(__name__)

class OrchestrationManager:
    """
    Manages the overall orchestration of agents and workflows.
    It initializes agents, manages their lifecycle, and handles the flow of requests.
    """
    def __init__(self, tool_manager: ToolManager, execution_log_service: ExecutionLogService):
        self.tool_manager = tool_manager
        self.execution_log_service = execution_log_service
        # Use a powerful model for the orchestrator, like gpt-4o or gpt-4
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=settings.openai_api_key) 
        
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """
        Initializes all specialized agents and registers them with the tool manager.
        The Master Orchestrator is initialized first to manage others.
        """
        # 1. Initialize the Master Orchestrator Agent
        # It needs a ToolManager that can provide descriptions of OTHER agents/tools.
        # We use the actual `tool_manager` instance here.
        master_orchestrator = MasterOrchestratorAgent(
            llm=self.llm,
            tool_manager=self.tool_manager, # Pass the actual tool manager
            execution_log_service=self.execution_log_service
        )
        self.agents[master_orchestrator.name] = master_orchestrator
        self.tool_manager.register_agent(master_orchestrator) # Register for other agents to find

        # 2. Initialize other specialized agents (these are defined in other files)
        # These agents will also need access to the tool_manager (to find other tools/agents)
        # and the execution_log_service.
        
        # Example: Sales Agent (Assuming SalesAgent class is imported and available)
        # from app.agents.sales_agent import SalesAgent
        # sales_agent = SalesAgent(llm=self.llm, tool_manager=self.tool_manager, execution_log_service=self.execution_log_service)
        # self.agents[sales_agent.name] = sales_agent
        # self.tool_manager.register_agent(sales_agent) # Register for orchestrator or other agents

        # Add other agents similarly:
        # from app.agents.support_agent import SupportAgent
        # support_agent = SupportAgent(llm=self.llm, tool_manager=self.tool_manager, execution_log_service=self.execution_log_service)
        # self.agents[support_agent.name] = support_agent
        # self.tool_manager.register_agent(support_agent)
        
        # from app.agents.project_manager_agent import ProjectManagerAgent
        # pm_agent = ProjectManagerAgent(llm=self.llm, tool_manager=self.tool_manager, execution_log_service=self.execution_log_service)
        # self.agents[pm_agent.name] = pm_agent
        # self.tool_manager.register_agent(pm_agent)

        # from app.agents.content_agent import ContentAgent
        # content_agent = ContentAgent(llm=self.llm, tool_manager=self.tool_manager, execution_log_service=self.execution_log_service)
        # self.agents[content_agent.name] = content_agent
        # self.tool_manager.register_agent(content_agent)
        
        logger.info(f"Initialized {len(self.agents)} agents.")

    async def process_message(self, user_input: str, conversation_id: int) -> Dict[str, Any]:
        """
        Processes a user message by activating the Master Orchestrator.
        This is the main entry point for handling incoming user requests.
        """
        logger.info(f"Processing message for conversation {conversation_id}: '{user_input}'")
        
        # Retrieve chat history for the conversation (placeholder)
        chat_history = await self._get_conversation_history(conversation_id)
        
        # Activate the Master Orchestrator Agent to handle the request
        orchestrator_agent = self.agents.get("Master Orchestrator")
        if not orchestrator_agent:
            logger.error("Master Orchestrator agent not found!")
            raise RuntimeError("Orchestration system not properly initialized: Master Orchestrator missing.")
        
        try:
            # The orchestrator will plan, delegate, and execute.
            # It needs the user input and potentially chat history.
            # The orchestrator's `run` method will return the final response.
            response_data = await orchestrator_agent.run(
                human_input=user_input,
                chat_history=chat_history,
                conversation_id=conversation_id # Pass conversation context
            )
            
            final_response = response_data.get("output", "An unexpected error occurred.")
            
            # Save the user message and agent response to conversation history (placeholder)
            await self._save_conversation_turn(conversation_id, user_input, final_response)
            
            logger.info(f"Message processed. Final response for conversation {conversation_id}: '{final_response}'")
            
            return {"response": final_response}

        except Exception as e:
            logger.error(f"Error processing message for conversation {conversation_id}: {e}", exc_info=True)
            # Log the error in execution logs too if possible
            # await self.execution_log_service.log_error(...)
            return {"error": f"An error occurred during processing: {str(e)}"}

    async def _get_conversation_history(self, conversation_id: int) -> List[BaseMessage]:
        """
        Retrieves the chat history for a given conversation from the database.
        Placeholder implementation.
        """
        logger.debug(f"Fetching chat history for conversation ID: {conversation_id} (placeholder)")
        # This would involve querying the database for messages associated with conversation_id.
        # Return as Langchain BaseMessage objects (HumanMessage, AIMessage).
        return []

    async def _save_conversation_turn(self, conversation_id: int, user_message: str, agent_response: str):
        """
        Saves the user's message and the agent's response to the conversation history in the database.
        Placeholder implementation.
        """
        logger.debug(f"Saving conversation turn for ID {conversation_id} (placeholder)")
        # This would involve creating Message records in the database.
        pass

# Instantiate the OrchestrationManager (will be done in main.py)
# orchestration_manager = OrchestrationManager(tool_manager=tool_manager, execution_log_service=MockExecutionLogService())
