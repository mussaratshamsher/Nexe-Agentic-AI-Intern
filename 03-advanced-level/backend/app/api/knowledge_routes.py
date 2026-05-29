from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.knowledge_schema import KnowledgeCreate, KnowledgeResponse
from app.services.knowledge_service import KnowledgeService
from typing import List

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

@router.get("/", response_model=List[KnowledgeResponse])
async def get_all_knowledge(db: AsyncSession = Depends(get_db)):
    service = KnowledgeService(db)
    return await service.get_all()

@router.post("/", response_model=KnowledgeResponse)
async def add_knowledge(knowledge_in: KnowledgeCreate, db: AsyncSession = Depends(get_db)):
    service = KnowledgeService(db)
    return await service.create(knowledge_in)
