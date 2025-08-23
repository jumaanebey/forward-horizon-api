import os
from typing import Optional
from app.calendar_service import GoogleCalendarService


class MessageSender:
    def __init__(self) -> None:
        self.scheduling_url: Optional[str] = os.getenv("SCHEDULING_URL")
        self.calendar_service = GoogleCalendarService()

    def send_sms(self, to_number: str, body: str) -> None:
        print(f"[SMS] -> {to_number}: {body}")

    def send_email(self, to_email: str, subject: str, body: str) -> None:
        print(f"[EMAIL] -> {to_email}: {subject}\n{body}")

    def call_to_action_text(self, lead_id: Optional[int] = None) -> str:
        if lead_id:
            booking_link = self.calendar_service.generate_booking_link(lead_id)
            return f"Book a quick video chat here: {booking_link}"
        elif self.scheduling_url:
            return f"Book a quick video chat here: {self.scheduling_url}"
        return "Reply YES to schedule a quick video chat."

    def get_available_slots(self):
        return self.calendar_service.get_available_slots()

    def schedule_meeting(self, lead_name: str, lead_email: str, slot_start: str) -> Optional[str]:
        return self.calendar_service.create_event(lead_name, lead_email, slot_start)