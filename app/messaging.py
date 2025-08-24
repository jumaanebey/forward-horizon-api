import os
from typing import Optional


class MessageSender:
    def __init__(self) -> None:
        self.scheduling_url: Optional[str] = os.getenv("SCHEDULING_URL")
        self.calendar_service = None  # Disabled for now, Google Calendar optional

    def send_sms(self, to_number: str, body: str) -> None:
        print(f"[SMS] -> {to_number}: {body}")

    def send_email(self, to_email: str, subject: str, body: str) -> None:
        print(f"[EMAIL] -> {to_email}: {subject}\n{body}")

    def call_to_action_text(self, lead_id: Optional[int] = None) -> str:
        if self.scheduling_url:
            return f"Book a quick video chat here: {self.scheduling_url}"
        return "Reply YES to schedule a quick video chat."

    def get_available_slots(self):
        return []  # Calendar integration disabled for now

    def schedule_meeting(self, lead_name: str, lead_email: str, slot_start: str) -> Optional[str]:
        return None  # Calendar integration disabled for now