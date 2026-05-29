from fastapi import APIRouter, Depends
from typing import List
from ..schemas.execution_schema import ExecutionLogResponse
from ..core.dependencies import get_execution_repo, get_current_user
from ..models.user_model import User

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/executions", response_model=List[ExecutionLogResponse])
async def get_execution_logs(
    skip: int = 0,
    limit: int = 100,
    execution_repo = Depends(get_execution_repo),
    current_user: User = Depends(get_current_user)
):
    return await execution_repo.get_all(skip, limit)
