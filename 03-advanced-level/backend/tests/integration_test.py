import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import AsyncSessionLocal
from app.repositories.knowledge_repository import KnowledgeRepository
from app.repositories.customer_repository import CustomerRepository
from app.services.chat_service import ChatService
from app.models.customer_model import Customer

async def test_workflow():
    async with AsyncSessionLocal() as db:
        print("🚀 Starting Real Integration Test...")
        
        # 1. Seed Knowledge Base
        kb_repo = KnowledgeRepository(db)
        await kb_repo.create(
            title="AI Automation Pricing 2024",
            content="Our Enterprise AI Automation plan costs $10,000 per month and includes 5 custom agents and 24/7 support.",
            category="Pricing"
        )
        print("✅ Seeded Knowledge Base")

        # 2. Create/Get Test Customer
        cust_repo = CustomerRepository(db)
        customer = await cust_repo.get_by_email("tester@example.com")
        if not customer:
            customer = await cust_repo.create({
                "name": "Test User",
                "email": "tester@example.com",
                "company": "Test Corp",
                "phone": "+1234567890"
            })
        print(f"✅ Using Customer: {customer.name} (ID: {customer.id})")

        # 3. Process Chat
        chat_service = ChatService(db)
        message = "Hi, I'm interested in your AI automation plans. Can you tell me the enterprise pricing and create a 3-week rollout plan?"
        
        print(f"\n💬 User: {message}")
        print("🤖 AI is thinking...\n")
        
        full_response = ""
        async for chunk in chat_service.process_chat(customer.id, message, channel="web"):
            if "|||" in chunk:
                # This is metadata
                continue
            full_response += chunk
            print(chunk, end="", flush=True)
        
        print("\n\n✅ Test Complete")
        
        # 4. Verify DB updates
        updated_customer = await cust_repo.get_by_id(customer.id)
        print(f"📊 Updated Lead Score: {updated_customer.lead_score}")
        print(f"📊 Updated Lead Status: {updated_customer.lead_status}")

if __name__ == "__main__":
    asyncio.run(test_workflow())
