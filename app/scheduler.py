import logging
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler

from app import db, faq
from app.messaging import MessageSender

logger = logging.getLogger(__name__)


class NudgeScheduler:
    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender
        self.scheduler = BackgroundScheduler()
        
    def start(self):
        if not self.scheduler.running:
            self.scheduler.add_job(
                func=self.send_nudges,
                trigger="interval",
                minutes=5,
                id="nudge_job",
                replace_existing=True,
            )
            self.scheduler.start()
            logger.info("Nudge scheduler started")
    
    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Nudge scheduler stopped")
    
    def send_nudges(self):
        due_leads = db.due_nudges(limit=10)
        
        for lead in due_leads:
            try:
                self._send_nudge_to_lead(lead)
                db.increment_nudges(lead["id"])
                
                if lead["nudges_sent"] < 2:
                    next_delay = 120 if lead["nudges_sent"] == 0 else 240
                    db.set_next_nudge(lead["id"], next_delay)
                else:
                    db.set_status(lead["id"], "cold")
                    
            except Exception as e:
                logger.error(f"Failed to send nudge to lead {lead['id']}: {e}")
    
    def _send_nudge_to_lead(self, lead):
        nudge_count = lead["nudges_sent"]
        
        if nudge_count == 0:
            message = f"Hi {lead['name']}, just wanted to follow up. {self.message_sender.call_to_action_text()}"
        elif nudge_count == 1:
            message = f"Hi {lead['name']}, still interested in chatting? {self.message_sender.call_to_action_text()}"
        else:
            message = f"Last chance, {lead['name']}! {self.message_sender.call_to_action_text()}"
        
        if lead["phone"]:
            self.message_sender.send_sms(lead["phone"], message)
            db.record_message(lead["id"], "outbound", "sms", message)
        elif lead["email"]:
            subject = "Following up" if nudge_count == 0 else "Still interested?" if nudge_count == 1 else "Last chance!"
            self.message_sender.send_email(lead["email"], subject, message)
            db.record_message(lead["id"], "outbound", "email", message)