from typing import List, Dict, Any
from ..schemas.task_schema import Task

class SessionMemory:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.tasks: Dict[str, Task] = {}
        self.context: Dict[str, Any] = {}

    def add_to_history(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def update_context(self, key: str, value: Any):
        self.context[key] = value

    def get_context(self) -> Dict[str, Any]:
        return self.context

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)

    def clear(self):
        self.history = []
        self.tasks = {}
        self.context = {}

# Global session memory for stage 1
session_memory = SessionMemory()
