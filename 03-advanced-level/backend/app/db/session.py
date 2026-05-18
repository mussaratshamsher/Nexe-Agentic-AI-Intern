from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator

async def get_db_session() -> Generator[AsyncSession, None, None]:
    """
    Dependency to provide an async database session.
    This function yields a session and ensures it's closed afterward.
    """
    # This part is duplicated from database.py to maintain module separation,
    # but ideally, this dependency function would be imported from database.py.
    # For clarity, we'll keep it here for now and refactor later if needed.
    from app.db.database import async_session_maker
    
    db_session = async_session_maker()
    try:
        yield db_session
    finally:
        await db_session.close()
