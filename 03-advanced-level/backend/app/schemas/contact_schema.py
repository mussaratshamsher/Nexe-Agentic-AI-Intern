from pydantic import BaseModel, EmailStr

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str
    company: str = "Website Visitor"

class ContactResponse(BaseModel):
    status: str
    message: str
