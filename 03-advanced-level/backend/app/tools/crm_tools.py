from typing import Dict, Any, List, Optional
from ..logs.execution_logger import ExecutionLogger
from ..repositories.customer_repository import CustomerRepository
from ..repositories.ticket_repository import TicketRepository
from ..schemas.ticket_schema import TicketCreate

class CRMTools:
    def __init__(self, db_session):
        self.cust_repo = CustomerRepository(db_session)
        self.ticket_repo = TicketRepository(db_session)

    async def create_customer(self, name: str, email: str, company: str = None) -> Dict[str, Any]:
        await ExecutionLogger.log("CRM System", f"Creating customer: {name} ({email})")
        customer = await self.cust_repo.create({
            "name": name,
            "email": email,
            "company": company
        })
        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "status": "active"
        }

    async def get_customer_history(self, email: str) -> List[Dict[str, Any]]:
        await ExecutionLogger.log("CRM System", f"Fetching history for: {email}")
        customer = await self.cust_repo.get_by_email(email)
        if not customer:
            return []
        
        # In a real app, you might fetch related messages or tickets
        return [
            {"date": str(customer.created_at), "action": "Account Created", "notes": f"Initial lead score: {customer.lead_score}"}
        ]

    async def create_ticket(self, customer_id: int, issue: str, priority: str = "medium") -> Dict[str, Any]:
        await ExecutionLogger.log("CRM System", f"Creating ticket for {customer_id}: {issue}")
        ticket_in = TicketCreate(
            customer_id=customer_id,
            issue_summary=issue,
            priority=priority
        )
        ticket = await self.ticket_repo.create(ticket_in)
        return {"ticket_id": ticket.id, "status": ticket.status, "priority": ticket.priority}

    async def get_open_tickets(self) -> List[Dict[str, Any]]:
        await ExecutionLogger.log("CRM System", "Fetching all open tickets")
        tickets = await self.ticket_repo.get_all()
        return [
            {"ticket_id": t.id, "subject": t.issue_summary, "status": t.status}
            for t in tickets if t.status == "open"
        ]
