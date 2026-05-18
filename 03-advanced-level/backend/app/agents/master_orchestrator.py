from typing import Dict, List, Any, Optional
from langchain_core.runnables import Runnable
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import Field
import json # For serializing details

from app.config.settings import settings
from app.agents.base_agent import BaseAgent # Our base agent class
from app.tools.tool_manager import ToolManager # To get available tools
from app.services.execution_log_service import ExecutionLogService # To log actions
from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Define the available tools that the Master Orchestrator might use
# For now, these are conceptual; actual tool implementations will be in `app/tools/`
# This agent will coordinate other agents, so its tools might include:
# - Task creation/delegation
# - Information retrieval (from CRM, Knowledge Base)
# - Agent lookup/management
# - Logging tool

# Mock tool definitions for demonstration purposes
@tool(args_schema=None) # No schema for this mock tool
def delegate_task_to_agent(agent_name: str, task_description: str, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delegates a specific task to another specialized agent.
    agent_name: The name of the agent to delegate to (e.g., 'Sales Agent', 'Support Agent').
    task_description: A brief description of the task.
    task_input: A dictionary containing the input parameters for the task.
    Returns the result from the delegated agent.
    """
    logger.info(f"Delegating task to {agent_name}: {task_description}")
    # In a real system, this would involve a call to the task delegation service
    # or directly invoking another agent's run method.
    # For now, it returns a mock response.
    return {"status": "delegated", "agent_name": agent_name, "task": task_description, "input_received": task_input, "mock_result": "Task processed by mock agent."}

@tool(args_schema=None) # No schema for this mock tool
def get_agent_capabilities(agent_name: str) -> Dict[str, Any]:
    """
    Retrieves the capabilities and description of a specific agent.
    agent_name: The name of the agent to query.
    Returns a dictionary describing the agent's purpose and tools.
    """
    logger.info(f"Getting capabilities for agent: {agent_name}")
    # In a real system, this would query an agent registry or metadata.
    # Mock response for now.
    return {"agent_name": agent_name, "description": f"This is a mock {agent_name} agent.", "tools": ["tool1", "tool2"]}


class MasterOrchestratorAgent(BaseAgent):
    """
    The Master Orchestrator Agent is the central brain of the system.
    It receives user requests, analyzes intent, plans workflows, delegates tasks
    to specialized agents, and synthesizes their outputs.
    """
    name: str = "Master Orchestrator"
    description: str = "The central agent responsible for understanding user requests, planning workflows, and delegating tasks to specialized agents."
    llm: BaseChatModel
    tools: List[tool] # Tools this agent can use
    tool_manager: ToolManager # To find and manage other agents/tools
    execution_log_service: ExecutionLogService # To log actions
    
    def __init__(self,
                 llm: BaseChatModel,
                 tool_manager: ToolManager,
                 execution_log_service: ExecutionLogService,
                 ):
        # Initialize tools that this agent directly uses
        # We also make other agents/tools discoverable via tool_manager
        agent_tools = [
            delegate_task_to_agent,
            get_agent_capabilities,
            # Potentially add tools for CRM, logging, etc. that the orchestrator needs directly
        ]
        super().__init__(name=self.name, description=self.description, llm=llm, tools=agent_tools)
        self.tool_manager = tool_manager
        self.execution_log_service = execution_log_service

    async def run(self, human_input: str, chat_history: List[BaseMessage] | None = None, **kwargs) -> Dict[str, Any]:
        """
        Receives user input, plans the workflow, and delegates tasks.
        """
        await self._log_execution("started", {"input": human_input})
        
        try:
            # Combine tools: The agent's own tools + tools from other agents accessible via ToolManager
            # This requires a way to map agent names/tasks to their respective tool definitions.
            # Langchain's agent creation typically handles this if tools are properly registered.
            
            # For a tools-based agent:
            # 1. Create a prompt that guides the agent.
            # 2. Create the agent using create_openai_tools_agent.
            # 3. Create an AgentExecutor to run the agent.

            # Agent needs access to all available tools, not just its own.
            # The 'tools' parameter in `create_openai_tools_agent` should be a list of all relevant tools.
            all_available_tools = self.tools + self.tool_manager.get_all_tools() # Simplistic approach
            
            # Prompt for the orchestrator agent
            # This prompt should guide the agent to analyze intent, plan, and delegate.
            # It needs to understand which agent is best suited for which task.
            orchestrator_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are the Master Orchestrator Agent. Your primary goal is to understand user requests,
                break them down into actionable tasks, and delegate these tasks to specialized agents.
                You have access to a suite of tools, including the ability to delegate tasks to other agents,
                query agent capabilities, and log execution steps.
                
                Available Agents and their descriptions:
                {agent_descriptions}

                When a user makes a request:
                1. Analyze the user's intent.
                2. If the request can be handled directly, use the appropriate tool.
                3. If the request requires specialized skills, identify the best agent(s) to delegate to.
                4. Use the `delegate_task_to_agent` tool to assign sub-tasks.
                5. Log all significant actions using the `log_execution_step` tool.
                6. Synthesize the final response based on the outcomes of delegated tasks or direct actions.
                
                Always aim to fulfill the user's request efficiently and accurately.
                If a request is ambiguous, ask for clarification.
                """),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}") # User's input
            ])

            # Get agent descriptions from the tool manager (or a registry)
            agent_descriptions_str = ""
            for agent_name, desc in self.tool_manager.get_agent_descriptions().items():
                agent_descriptions_str += f"- {agent_name}: {desc}
"

            # Create the agent executor
            # This requires a specific agent implementation from Langchain that uses tools
            # `create_openai_tools_agent` is a good fit.
            agent = create_openai_tools_agent(
                llm=self.llm,
                tools=all_available_tools, # Pass all tools the agent can use
                prompt=orchestrator_prompt.partial(agent_descriptions=agent_descriptions_str)
            )
            
            # Use RunnableWithMessageHistory for managing chat history
            # This is a conceptual implementation. Actual history management depends on `chat_history` input.
            message_history = ChatMessageHistory(messages=chat_history if chat_history else [])
            agent_with_history = RunnableWithMessageHistory(
                agent,
                lambda config: message_history, # Function to get message history
                input_messages_key="input",
                history_messages_key="chat_history"
            )

            # The AgentExecutor orchestrates the agent's interaction with tools
            # We need a way to map the agent's output to the correct `invoke` method.
            # For demonstration, we'll use a simplified AgentExecutor and `agent_with_history.invoke`
            
            # In a real scenario, AgentExecutor from `langchain.agents` would be used.
            # Here, we simulate by invoking the Runnable directly.
            # The input to the agent typically needs to be in a dict format.
            
            # Create a Langchain AgentExecutor (this is the standard way)
            agent_executor_instance = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=all_available_tools,
                verbose=settings.debug, # Set to True to see agent thought process
                handle_parsing_errors=True # Gracefully handle errors from tool calls
            )

            # Invoke the agent executor.
            # The input structure depends on how the RunnableWithMessageHistory is configured.
            # It expects keys like 'input' and 'chat_history'.
            agent_response = await agent_executor_instance.invoke(
                {"input": human_input, "chat_history": chat_history if chat_history else []}
            )

            # Log the outcome
            final_response_content = agent_response.get("output", "Orchestrator did not produce a final output.")
            await self._log_execution("completed", {"output": final_response_content, "agent_response_details": json.dumps(agent_response)})

            return {"output": final_response_content}

        except Exception as e:
            await self._log_execution("failed", {"error": str(e), "details": json.dumps(getattr(e, 'response', {}))})
            logger.error(f"Master Orchestrator agent failed: {e}", exc_info=True)
            # Raise a specific exception or re-raise the original one
            raise InternalServerErrorException(detail=f"Master Orchestrator failed: {e}") from e

# --- Helper to get agent names and descriptions for the prompt ---
# This would be managed by the ToolManager or a dedicated AgentRegistry
# For now, we'll define them here and assume ToolManager will access them.
# In a real app, this would be dynamically loaded.

# Placeholder for ToolManager and ExecutionLogService, these will be implemented later
class MockToolManager:
    def get_all_tools(self) -> List[tool]:
        # Return tools from all registered agents + core tools
        # This mock includes delegate_task_to_agent and get_agent_capabilities.
        # Later, it will dynamically load tools from other agents.
        return [delegate_task_to_agent, get_agent_capabilities] # Mock tools

    def get_agent_descriptions(self) -> Dict[str, str]:
        return {
            "Master Orchestrator": "The central agent responsible for understanding user requests, planning workflows, and delegating tasks to specialized agents.",
            "Support Agent": "Handles customer support inquiries, FAQs, and ticket generation.",
            "Sales Agent": "Qualifies leads, recommends services, and analyzes inquiries.",
            "Project Manager Agent": "Performs multi-step reasoning, project planning, and task decomposition.",
            "Content Agent": "Generates proposals and drafts communications."
        }

class MockExecutionLogService:
    def __init__(self):
        self.logger = setup_logger("mock_execution_log_service")

    async def log_execution_step(self, agent_name: str, action: str, status: str, details: Optional[Dict] = None):
        self.logger.info(f"[{agent_name}] {action} - Status: {status} - Details: {details}")
        # In a real implementation, this would save to the database.
        pass

