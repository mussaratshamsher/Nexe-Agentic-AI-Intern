from typing import List, Dict
from ..logs.execution_logger import ExecutionLogger
from ..repositories.knowledge_repository import KnowledgeRepository

class KnowledgeTools:
    def __init__(self, db_session):
        self.kb_repo = KnowledgeRepository(db_session)

    async def search_knowledge_base(self, query: str) -> str:
        await ExecutionLogger.log("Knowledge Base", f"RAG search for: {query}")
        results = await self.kb_repo.search(query)
        
        if not results:
            return "No specific information found in the internal knowledge base. Please check external sources or escalate to a manager."
        
        formatted_results = "\n---\n".join([f"Source: {r.title}\nContent: {r.content}" for r in results])
        return f"Found relevant information in internal knowledge base:\n{formatted_results}"
