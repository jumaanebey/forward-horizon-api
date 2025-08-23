from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import db, faq, messaging, models
from app.scheduler import NudgeScheduler

app = FastAPI(title="Lead Funnel API", version="1.0.0")

message_sender = messaging.MessageSender()
nudge_scheduler = NudgeScheduler(message_sender=message_sender)


@app.on_event("startup")
async def startup_event():
    db.init_db()
    nudge_scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    nudge_scheduler.stop()


@app.post("/leads", response_model=models.LeadOut)
def create_lead(lead: models.LeadCreate):
    lead_id = db.create_lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        source=lead.source,
    )
    
    welcome_message = f"Hi {lead.name}! Thanks for your interest. {message_sender.call_to_action_text()}"
    
    if lead.phone:
        message_sender.send_sms(lead.phone, welcome_message)
        db.record_message(lead_id, "outbound", "sms", welcome_message)
    elif lead.email:
        subject = "Welcome! Let's schedule a quick chat"
        message_sender.send_email(lead.email, subject, welcome_message)
        db.record_message(lead_id, "outbound", "email", welcome_message)
    
    db.set_next_nudge(lead_id, 60)
    
    created_lead = db.get_lead(lead_id)
    return models.LeadOut(**created_lead)


@app.post("/webhooks/inbound")
def handle_inbound_message(message: models.InboundMessage):
    lead = db.get_lead(message.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.record_message(message.lead_id, "inbound", message.channel, message.content)
    
    content_lower = message.content.lower()
    
    if "yes" in content_lower or "schedule" in content_lower:
        if message_sender.scheduling_url:
            db.set_scheduled(message.lead_id, message_sender.scheduling_url)
            response = f"Perfect! Here's your scheduling link: {message_sender.scheduling_url}"
        else:
            db.set_status(message.lead_id, "interested")
            response = "Great! Someone from our team will reach out soon to schedule."
        
        if message.channel == "sms" and lead["phone"]:
            message_sender.send_sms(lead["phone"], response)
        elif message.channel == "email" and lead["email"]:
            message_sender.send_email(lead["email"], "Scheduling your chat", response)
        
        db.record_message(message.lead_id, "outbound", message.channel, response)
        
    elif "no" in content_lower or "stop" in content_lower or "cancel" in content_lower:
        db.set_status(message.lead_id, "unsubscribed")
        response = "No problem! You've been removed from our follow-up list."
        
        if message.channel == "sms" and lead["phone"]:
            message_sender.send_sms(lead["phone"], response)
        elif message.channel == "email" and lead["email"]:
            message_sender.send_email(lead["email"], "You're all set", response)
        
        db.record_message(message.lead_id, "outbound", message.channel, response)
        
    else:
        faq_answer = faq.answer_for(message.content)
        if faq_answer:
            if message.channel == "sms" and lead["phone"]:
                message_sender.send_sms(lead["phone"], faq_answer)
            elif message.channel == "email" and lead["email"]:
                message_sender.send_email(lead["email"], "Quick answer", faq_answer)
            
            db.record_message(message.lead_id, "outbound", message.channel, faq_answer)
        else:
            generic_response = f"Thanks for your message! {message_sender.call_to_action_text()}"
            
            if message.channel == "sms" and lead["phone"]:
                message_sender.send_sms(lead["phone"], generic_response)
            elif message.channel == "email" and lead["email"]:
                message_sender.send_email(lead["email"], "Thanks for reaching out", generic_response)
            
            db.record_message(message.lead_id, "outbound", message.channel, generic_response)
    
    return {"status": "processed"}


@app.post("/webhooks/scheduled")
def trigger_scheduled_nudges():
    nudge_scheduler.send_nudges()
    return {"status": "nudges_sent"}


@app.get("/calendar/available-slots")
def get_available_slots():
    slots = message_sender.get_available_slots()
    return {"available_slots": slots}


@app.post("/calendar/book-meeting")
def book_meeting(lead_id: int, slot_start: str):
    lead = db.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    meeting_link = message_sender.schedule_meeting(
        lead_name=lead["name"],
        lead_email=lead["email"],
        slot_start=slot_start
    )
    
    if meeting_link:
        db.set_scheduled(lead_id, meeting_link)
        
        confirmation_message = f"Great! Your meeting is confirmed. Details: {meeting_link}"
        
        if lead["phone"]:
            message_sender.send_sms(lead["phone"], confirmation_message)
            db.record_message(lead_id, "outbound", "sms", confirmation_message)
        elif lead["email"]:
            message_sender.send_email(lead["email"], "Meeting Confirmed", confirmation_message)
            db.record_message(lead_id, "outbound", "email", confirmation_message)
        
        return {"status": "booked", "meeting_link": meeting_link}
    else:
        raise HTTPException(status_code=500, detail="Failed to create meeting")


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}