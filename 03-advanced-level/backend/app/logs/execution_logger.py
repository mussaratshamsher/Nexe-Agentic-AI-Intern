from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from typing import Optional
from ..repositories.execution_repository import ExecutionRepository
from ..schemas.execution_schema import ExecutionLogCreate

console = Console()

class ExecutionLogger:
    @staticmethod
    async def log(agent_name: str, action: str, details: str = None, repo: Optional[ExecutionRepository] = None, reasoning: str = None, step_number: int = 1):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = "green"
        # ... (rest of colors)
        if "Orchestrator" in agent_name:
            color = "cyan"
        elif "Sales" in agent_name:
            color = "yellow"
        elif "PM" in agent_name:
            color = "magenta"
        elif "Content" in agent_name:
            color = "blue"
        elif "Support" in agent_name:
            color = "red"

        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append(f"{agent_name}: ", style=f"bold {color}")
        text.append(action)
        if details:
            text.append(f" -> {details}", style="italic")
        
        console.print(text)

        if repo:
            log_in = ExecutionLogCreate(
                agent_name=agent_name,
                action=action,
                details=details,
                reasoning=reasoning,
                step_number=step_number
            )
            await repo.create(log_in)

    @staticmethod
    def display_final_response(response: str):
        console.print(Panel(response, title="Final Response", border_style="bold green"))
