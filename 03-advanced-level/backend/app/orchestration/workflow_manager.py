from ..agents.orchestrator import OrchestratorAgent
from ..agents.sales_agent import SalesAgent
from ..agents.support_agent import SupportAgent
from ..agents.pm_agent import PMAgent
from ..agents.content_agent import ContentAgent
from ..logs.execution_logger import ExecutionLogger
from ..memory.session_memory import session_memory

class WorkflowManager:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.agents = {
            "Sales": SalesAgent(),
            "Support": SupportAgent(),
            "PM": PMAgent(),
            "Content": ContentAgent()
        }

    async def execute_workflow(self, user_request: str):
        # 1. Plan
        plan_data = await self.orchestrator.analyze_and_plan(user_request)
        
        agent_outputs = []
        
        # 2. Delegate and Execute
        for step in plan_data.get("plan", []):
            agent_name = step.get("agent")
            task_desc = step.get("task")
            
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                output = await agent.run(task_desc)
                agent_outputs.append({
                    "agent": agent_name,
                    "output": output
                })
            else:
                ExecutionLogger.log("System", f"Warning: Agent {agent_name} not found", "Skipping step")

        # 3. Synthesize
        final_response = await self.orchestrator.synthesize(user_request, agent_outputs)
        
        # Update memory
        session_memory.add_to_history("user", user_request)
        session_memory.add_to_history("assistant", final_response)
        
        return final_response
