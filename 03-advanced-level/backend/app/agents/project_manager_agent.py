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

# Mock tools for Project Manager Agent
@tool(args_schema=None)
def decompose_task(task_description: str) -> Dict[str, Any]:
    """
    Decomposes a large task into smaller, manageable sub-tasks.
    Returns a list of sub-task descriptions.
    """
    logger.info(f"Mock: Decomposing task: {task_description}")
    if "build a website" in task_description.lower():
        return {"sub_tasks": ["Design UI/UX", "Develop frontend", "Develop backend", "Deploy application"]}
    else:
        return {"sub_tasks": ["Understand requirements", "Execute task", "Review results"]}

@tool(args_schema=None)
def generate_project_timeline(sub_tasks: List[str], estimated_durations: Dict[str, int]) -> Dict[str, Any]:
    """
    Generates a project timeline based on sub-tasks and their estimated durations.
    Returns a list of tasks with planned start and end dates.
    """
    logger.info(f"Mock: Generating timeline for tasks: {sub_tasks}, durations: {estimated_durations}")
    # Simple timeline generation
    timeline = []
    current_date = 1 # Start day
    for task in sub_tasks:
        duration = estimated_durations.get(task, 1) # Default duration of 1 day
        start_date = current_date
        end_date = current_date + duration - 1
        timeline.append({"task": task, "start_date": f"Day {start_date}", "end_date": f"Day {end_date}"})
        current_date += duration
    return {"timeline": timeline}

class ProjectManagerAgent(BaseAgent):
    name: str = "Project Manager Agent"
    description: str = "Responsible for multi-step reasoning, project planning, and task decomposition."
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
            decompose_task,
            generate_project_timeline,
        ]
        super().__init__(name=self.name, description=self.description, llm=llm, tools=agent_tools)
        self.tool_manager = tool_manager
        self.execution_log_service = execution_log_service

    async def run(self, human_input: str, chat_history: List[BaseMessage] | None = None, **kwargs) -> Dict[str, Any]:
        """
        Handles project planning and task decomposition.
        """
        await self._log_execution("started", {"input": human_input})
        
        try:
            all_available_tools = self.tools + self.tool_manager.get_all_tools()
            
            pm_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are the Project Manager Agent. Your role is to help plan projects, decompose tasks, and generate timelines.
                You have access to tools for task decomposition and timeline generation.
                When a user asks for project planning or task breakdown:
                1. Understand the overall project goal.
                2. Use `decompose_task` to break down the main goal into smaller steps.
                3. If duration information is needed for timeline generation, ask the user for estimates or use defaults.
                4. Use `generate_project_timeline` to create a schedule.
                5. Log all significant actions using `log_execution_step`.
                6. Present the plan and timeline clearly to the user.
                """),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}")
            ])
            
            agent = create_openai_tools_agent(
                llm=self.llm,
                tools=all_available_tools,
                prompt=pm_prompt
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
            
            final_response_content = agent_response.get("output", "Project Manager agent did not produce a final output.")
            await self._log_execution("completed", {"output": final_response_content, "agent_response_details": json.dumps(agent_response)})
            
            return {"output": final_response_content}

        except Exception as e:
            await self._log_execution("failed", {"error": str(e), "details": json.dumps(getattr(e, 'response', {}))})
            logger.error(f"Project Manager Agent failed: {e}", exc_info=True)
            raise InternalServerErrorException(detail=f"Project Manager Agent failed: {e}") from e
