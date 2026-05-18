from typing import List, Dict, Any
from langchain_core.tools import tool # Type hint for tools

from app.logs.logger import setup_logger
# Import all tool modules
from .crm_tools import (
    create_customer, get_customer_history, create_ticket, get_open_tickets
)
from .knowledge_tools import search_knowledge_base
from .logging_tools import log_execution_step
from .communication_tools import send_email, send_whatsapp_message
# Import base agent class and mock manager for orchestrator agent
from app.agents.base_agent import BaseAgent, AgentExecutor # For type hints and structure
from app.agents.master_orchestrator import MockToolManager as OrchestratorMockToolManager # Use mock for orchestrator init

logger = setup_logger(__name__)

class ToolManager:
    """
    Manages the registration, retrieval, and discovery of all available tools and agents.
    This allows agents to dynamically find and use tools/agents they need.
    """
    def __init__(self):
        self._tools: Dict[str, tool] = {}
        self._agents: Dict[str, BaseAgent] = {} # Stores actual agent instances
        self._agent_descriptions: Dict[str, str] = {} # Stores descriptions for prompts
        self._register_tools()
        # We will register agents dynamically or after they are instantiated.
        # For now, we use a mock for the orchestrator's init.

    def _register_tools(self):
        """Registers all available tools."""
        # Dynamically register tools by inspecting imported modules
        # This is a simplified approach; a more robust system might use entry points or config files.

        # CRM Tools
        self._register_tool(create_customer)
        self._register_tool(get_customer_history)
        self._register_tool(create_ticket)
        self._register_tool(get_open_tickets)

        # Knowledge Tools
        self._register_tool(search_knowledge_base)

        # Logging Tools
        self._register_tool(log_execution_step)

        # Communication Tools
        self._register_tool(send_email)
        self._register_tool(send_whatsapp_message)

        logger.info(f"Registered {len(self._tools)} tools.")

    def _register_tool(self, tool_func):
        """Helper to register a single tool."""
        if hasattr(tool_func, '__name__') and hasattr(tool_func, 'name') and hasattr(tool_func, 'description'):
            tool_name = getattr(tool_func, 'name') # Langchain tool name
            if tool_name in self._tools:
                logger.warning(f"Tool '{tool_name}' already registered. Overwriting.")
            self._tools[tool_name] = tool_func
        else:
            logger.warning(f"Could not register tool: {tool_func}. Missing required attributes (__name__, name, description).")

    def get_all_tools(self) -> List[tool]:
        """Returns a list of all registered tools."""
        return list(self._tools.values())

    def get_tool_by_name(self, name: str) -> Optional[tool]:
        """Returns a specific tool by its name."""
        return self._tools.get(name)

    def register_agent(self, agent: BaseAgent):
        """Registers an agent instance."""
        if agent.name in self._agents:
            logger.warning(f"Agent '{agent.name}' already registered. Overwriting.")
        self._agents[agent.name] = agent
        self._agent_descriptions[agent.name] = agent.description
        logger.info(f"Registered agent: {agent.name}")

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Retrieves an agent instance by name."""
        return self._agents.get(name)

    def get_all_agent_names(self) -> List[str]:
        """Returns a list of names of all registered agents."""
        return list(self._agents.keys())

    def get_agent_descriptions(self) -> Dict[str, str]:
        """Returns a dictionary of agent names and their descriptions for prompts."""
        return self._agent_descriptions

    # Note: For the Master Orchestrator's initialization, we currently use a mock
    # tool manager to provide agent descriptions. This `ToolManager` instance
    # will be populated with actual agent instances later, allowing the orchestrator
    # to dynamically discover and delegate tasks.
    # For now, this manager is intended to be instantiated once and shared.
    # The orchestrator's __init__ needs a tool_manager that can provide descriptions.
    # A better approach might be dependency injection where the tool_manager is passed.

# Singleton instance of ToolManager
# This instance will be created once and shared across the application.
# It will be used to provide tools to agents and manage agent registry.
tool_manager = ToolManager()

# --- Initial registration for the orchestrator's mock ---
# This is a workaround because the orchestrator needs to know about other agents
# before they are fully instantiated and registered in the tool_manager.
# This mock will be replaced by a real one once agents are set up.
# We'll use OrchestratorMockToolManager directly for the orchestrator's __init__
# and then populate the real tool_manager instance later.
