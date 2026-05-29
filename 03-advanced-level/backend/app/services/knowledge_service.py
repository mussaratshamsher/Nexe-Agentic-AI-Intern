from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.knowledge_model import KnowledgeBase
from app.schemas.knowledge_schema import KnowledgeCreate, KnowledgeUpdate
from typing import List, Optional

class KnowledgeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[KnowledgeBase]:
        result = await self.db.execute(select(KnowledgeBase))
        return result.scalars().all()

    async def create(self, knowledge_in: KnowledgeCreate) -> KnowledgeBase:
        db_knowledge = KnowledgeBase(**knowledge_in.model_dump())
        self.db.add(db_knowledge)
        await self.db.commit()
        await self.db.refresh(db_knowledge)
        return db_knowledge

    async def search(self, query: str) -> List[KnowledgeBase]:
        # Simple text-based search for now
        # In a real RAG system, this would use vector embeddings
        result = await self.db.execute(
            select(KnowledgeBase).where(
                (KnowledgeBase.title.contains(query)) | (KnowledgeBase.content.contains(query))
            )
        )
        return result.scalars().all()
