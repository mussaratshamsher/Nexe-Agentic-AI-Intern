import asyncio
from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base

async def init_models():
    async with engine.begin() as conn:
        print("Enabling pgvector extension...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())
