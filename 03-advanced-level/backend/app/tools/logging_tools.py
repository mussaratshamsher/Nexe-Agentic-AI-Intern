from ..logs.execution_logger import ExecutionLogger
from ..schemas.task_schema import ExecutionStep

class LoggingTools:
    @staticmethod
    async def log_execution_step(agent_name: str, action: str, details: str = None):
        step = ExecutionStep(agent_name=agent_name, action=action, details=details)
        ExecutionLogger.log_step(step)
        return True
