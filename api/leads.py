from fastapi import FastAPI, HTTPException
from datetime import datetime
import json
import os

app = FastAPI()

# For now, we'll store in memory (later can upgrade to Vercel KV or PostgreSQL)
leads_storage = []

@app.post("/api/leads/submit")
async def submit_lead(name: str, email: str = None, phone: str = None, message: str = None):
    """Store lead and send notification"""
    
    lead = {
        "id": len(leads_storage) + 1,
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "created_at": datetime.now().isoformat(),
        "status": "new"
    }
    
    leads_storage.append(lead)
    
    # TODO: Send email notification
    # TODO: Add to CRM
    # TODO: Send SMS confirmation
    
    return {
        "success": True,
        "message": f"Thank you {name}! We'll contact you within 24 hours.",
        "lead_id": lead["id"]
    }

@app.get("/api/leads/list")
async def list_leads(secret: str = None):
    """List all leads (protected endpoint)"""
    
    # Simple protection - in production use proper auth
    if secret != os.environ.get("ADMIN_SECRET", "your-secret-key"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return {
        "total": len(leads_storage),
        "leads": leads_storage
    }

@app.get("/api/leads/stats")
async def lead_stats():
    """Get lead statistics"""
    
    return {
        "total_leads": len(leads_storage),
        "today": len([l for l in leads_storage if l["created_at"].startswith(datetime.now().strftime("%Y-%m-%d"))]),
        "status": "operational"
    }