from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Mock knowledge base service
class MockKnowledgeBaseService:
    def search(self, query: str) -> Dict[str, Any]:
        logger.info(f"Mock: Searching knowledge base for query: '{query}'")
        if "AI Business Operations Manager" in query:
            return {"query": query, "results": [{"title": "AI BOM Overview", "content": "The AI Business Operations Manager is a SaaS platform designed to automate business operations using AI agents."}]}
        elif "FastAPI" in query:
            return {"query": query, "results": [{"title": "FastAPI Documentation", "content": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+."}]}
        else:
            return {"query": query, "results": []}

knowledge_base_service = MockKnowledgeBaseService()

class SearchKnowledgeBaseArgs(BaseModel):
    query: str = Field(..., description="The search query for the knowledge base")

@tool(args_schema=SearchKnowledgeBaseArgs, tool_name="search_knowledge_base")
def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Searches the internal knowledge base for information.
    Useful for answering questions about the platform, technologies, or general business processes.
    """
    return knowledge_base_service.search(query=query)
