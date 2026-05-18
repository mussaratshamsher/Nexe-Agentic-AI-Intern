from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# Database URL from settings
DATABASE_URL = settings.database_url

# Create an async engine
# The pool_size and max_overflow parameters can be tuned for production.
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=settings.debug, # Set to True to see SQL queries during debugging
    future=True # Recommended for SQLAlchemy 2.0+
)

# Create a configured "sessionmaker" for async sessions
# expire_on_commit=False is important for async operations
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    """
    Dependency to provide an async database session.
    This function yields a session and ensures it's closed afterward.
    """
    # Import your ORM models here to ensure they are registered with metadata
    # when SQLAlchemy initializes. This is a placeholder.
    # Actual imports will be explicit in models/__init__.py or where Base is defined.
    # Example: from . import user, customer, conversation, message, ticket, execution_log, task
    
    db_session = async_session_maker()
    try:
        yield db_session
    finally:
        await db_session.close()

# Function to create all tables (for initial setup or testing)
# In a real application, migrations (e.g., with Alembic) are preferred for production.
# This function will be called during startup or via a management script.
async def create_tables():
    async with engine.begin() as conn:
        # Import models here to ensure they are included in metadata
        # This is a common pattern to trigger model registration.
        # For now, it's a placeholder. Alembic will handle migrations in production.
        pass # Placeholder: actual model creation will be handled by Alembic or explicit calls.
