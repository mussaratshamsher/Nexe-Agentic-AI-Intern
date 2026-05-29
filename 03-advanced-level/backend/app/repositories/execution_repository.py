from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ..models.execution_log_model import ExecutionLog
from ..schemas.execution_schema import ExecutionLogCreate

class ExecutionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, log_in: ExecutionLogCreate) -> ExecutionLog:
        db_log = ExecutionLog(**log_in.model_dump())
        self.db.add(db_log)
        await self.db.commit()
        await self.db.refresh(db_log)
        return db_log

    async def log_action(self, agent_name: str, action: str, status: str, details: str = None, reasoning: str = None, step_number: int = 1) -> ExecutionLog:
        log_in = ExecutionLogCreate(agent_name=agent_name, action=action, status=status, details=details, reasoning=reasoning, step_number=step_number)
        return await self.create(log_in)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ExecutionLog]:
        query = select(ExecutionLog).order_by(ExecutionLog.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
