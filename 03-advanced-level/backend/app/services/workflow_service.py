from typing import List, Optional
from ..agents.stage1_agents.orchestrator import OrchestratorAgent
from ..agents.stage1_agents.sales_agent import SalesAgent
from ..agents.stage1_agents.support_agent import SupportAgent
from ..agents.stage1_agents.pm_agent import PMAgent
from ..agents.stage1_agents.content_agent import ContentAgent
from ..repositories.execution_repository import ExecutionRepository
from ..logs.execution_logger import ExecutionLogger

class WorkflowService:
    def __init__(self, execution_repo: ExecutionRepository):
        self.execution_repo = execution_repo
        self.orchestrator = OrchestratorAgent()
        self.agents = {
            "Sales": SalesAgent(),
            "Support": SupportAgent(),
            "PM": PMAgent(),
            "Content": ContentAgent()
        }

    async def run_workflow(self, user_request: str) -> str:
        await ExecutionLogger.log("System", "Workflow started", user_request[:50] + "...", self.execution_repo)
        
        # 1. Plan
        plan_data = await self.orchestrator.analyze_and_plan(user_request, self.execution_repo)
        
        agent_outputs = []
        
        # 2. Delegate and Execute
        for step in plan_data.get("plan", []):
            agent_name = step.get("agent")
            task_desc = step.get("task")
            
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                await ExecutionLogger.log("System", f"Delegating to {agent_name}", task_desc[:50] + "...", self.execution_repo)
                output = await agent.run(task_desc, repo=self.execution_repo)
                agent_outputs.append({
                    "agent": agent_name,
                    "output": output
                })
            else:
                await ExecutionLogger.log("System", f"Warning: Agent {agent_name} not found", "Skipping step", self.execution_repo)

        # 3. Synthesize
        final_response = await self.orchestrator.synthesize(user_request, agent_outputs, self.execution_repo)
        await ExecutionLogger.log(self.orchestrator.name, "Final response synthesized", "Workflow complete", self.execution_repo)
        
        return final_response
