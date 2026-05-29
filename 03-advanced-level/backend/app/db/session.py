from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Force usage of asyncpg and clean URL
url = settings.DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
# If it's just postgresql (no driver specified), append +asyncpg
if "://" in url and "+" not in url.split("://")[0]:
    url = url.replace("postgresql://", "postgresql+asyncpg://")

# Remove sslmode=require as asyncpg doesn't support it in the query string
if "sslmode=" in url:
    import re
    url = re.sub(r'[?&]sslmode=[^&]*', '', url)

engine = create_async_engine(url, echo=True, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
