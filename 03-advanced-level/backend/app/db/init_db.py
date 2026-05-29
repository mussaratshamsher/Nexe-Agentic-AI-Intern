from .session import engine
from .base import Base
# Import all models to ensure they are registered with Base.metadata
from ..models.user_model import User
from ..models.customer_model import Customer
from ..models.conversation_model import Conversation
from ..models.message_model import Message
from ..models.ticket_model import Ticket
from ..models.execution_log_model import ExecutionLog
from ..models.task_model import Task

def init_db():
    print("Connecting to database...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
