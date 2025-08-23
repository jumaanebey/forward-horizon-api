from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None


class LeadOut(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: str
    scheduled_url: Optional[str] = None


class InboundMessage(BaseModel):
    lead_id: int
    channel: str = Field(..., pattern=r"^(sms|email)$")
    content: str = Field(..., min_length=1)