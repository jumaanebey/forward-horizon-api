from fastapi import FastAPI
import os
from datetime import datetime

app = FastAPI()

@app.post("/api/notify/email")
async def send_email_notification(lead_name: str, lead_email: str, lead_phone: str = None):
    """Send email notification when new lead comes in"""
    
    # For production, use SendGrid, Postmark, or Resend
    # For now, we'll return what would be sent
    
    notification = {
        "to": "info@theforwardhorizon.com",  # Your email
        "subject": f"New Lead: {lead_name}",
        "body": f"""
        New lead received from Forward Horizon website:
        
        Name: {lead_name}
        Email: {lead_email}
        Phone: {lead_phone or 'Not provided'}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Please follow up within 24 hours.
        """,
        "status": "ready_to_send"
    }
    
    # TODO: Actually send email using email service
    # Example with Resend (they have free tier):
    # import resend
    # resend.api_key = os.environ.get("RESEND_API_KEY")
    # resend.Emails.send(notification)
    
    return notification

@app.post("/api/notify/sms")
async def send_sms_notification(lead_name: str, to_phone: str):
    """Send SMS confirmation to lead"""
    
    # For production use Twilio or similar
    sms = {
        "to": to_phone,
        "message": f"Hi {lead_name}, thanks for contacting Forward Horizon! We'll call you within 24 hours to discuss your project.",
        "status": "ready_to_send"
    }
    
    return sms