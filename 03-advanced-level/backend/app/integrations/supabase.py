from supabase import create_client, Client
from app.config.settings import settings
from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Supabase client initialization
# The anon key is typically used for client-side SDKs, but we can use it for some
# backend operations if Row Level Security (RLS) is configured appropriately.
# For full backend access (e.g., bypassing RLS), the service role key is needed.
# We will prioritize the service role key for backend operations.

SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_service_role_key # Use service role key for backend

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("Supabase URL or Service Role Key not configured. Supabase integration will be disabled.")
    supabase_client: Client | None = None
else:
    try:
        # The supabase-py client library is not async by default.
        # For async operations, we might need to wrap its calls or use a different approach
        # if direct async support is critical. However, for simple CRUD operations,
        # it might be acceptable to run sync calls in an async context if performance
        # is not extremely sensitive for these specific calls, or use a separate async library.
        # For now, we initialize the standard client.
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        supabase_client = None

# Function to get the Supabase client, handling potential None case
def get_supabase_client() -> Client:
    if supabase_client is None:
        raise ConnectionError("Supabase client is not initialized. Please check configuration.")
    return supabase_client

# Example of how to use Supabase in a service or repository:
# async def get_user_from_supabase(user_id: int):
#     if supabase_client:
#         # Example: Fetch user from 'users' table in Supabase
#         # Note: supabase-py client is synchronous. For async, you'd typically
#         # run sync calls in a thread pool executor or use an async http client.
#         # For simplicity here, assuming it's called from an async context that can handle it.
#         try:
#             response = supabase_client.table("users").select("*").eq("id", user_id).execute()
#             if response.data:
#                 return response.data[0]
#             else:
#                 return None
#         except Exception as e:
#             logger.error(f"Error querying Supabase users table: {e}")
#             return None
#     return None
