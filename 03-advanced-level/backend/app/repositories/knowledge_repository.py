from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.models.knowledge_model import KnowledgeBase
from app.services.embedding_service import EmbeddingService
from typing import List, Optional

class KnowledgeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, query: str, limit: int = 3) -> List[KnowledgeBase]:
        # Generate embedding for the query
        query_embedding = EmbeddingService.get_embedding(query)
        
        # Semantic search using cosine similarity via pgvector
        # l2_distance (<->), max_inner_product (<#>), or cosine_distance (<=>)
        result = await self.db.execute(
            select(KnowledgeBase)
            .order_by(KnowledgeBase.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, title: str, content: str, category: str = None) -> KnowledgeBase:
        # Automatically generate embedding for new content
        embedding = EmbeddingService.get_embedding(f"{title}: {content}")
        
        db_item = KnowledgeBase(
            title=title, 
            content=content, 
            category=category,
            embedding=embedding
        )
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item
