import os
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.calendar_id = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
        self._authenticate()
    
    def _authenticate(self):
        creds = None
        
        # Load credentials from environment variable (for production)
        if os.getenv('GOOGLE_CREDENTIALS_JSON'):
            creds_data = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # For development - use credentials.json file
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    raise Exception("Google Calendar credentials not found. Set GOOGLE_CREDENTIALS_JSON or provide credentials.json")
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def get_available_slots(self, days_ahead: int = 7, duration_minutes: int = 30) -> List[Dict[str, Any]]:
        """Get available time slots for scheduling"""
        now = datetime.utcnow()
        end_time = now + timedelta(days=days_ahead)
        
        # Get busy times
        body = {
            "timeMin": now.isoformat() + 'Z',
            "timeMax": end_time.isoformat() + 'Z',
            "items": [{"id": self.calendar_id}]
        }
        
        events_result = self.service.freebusy().query(body=body).execute()
        busy_times = events_result['calendars'][self.calendar_id]['busy']
        
        # Generate available slots (9 AM - 5 PM, weekdays)
        available_slots = []
        current = now.replace(hour=9, minute=0, second=0, microsecond=0)
        
        while current < end_time:
            # Skip weekends
            if current.weekday() >= 5:
                current += timedelta(days=1)
                current = current.replace(hour=9, minute=0)
                continue
            
            # Skip past business hours
            if current.hour >= 17:
                current += timedelta(days=1)
                current = current.replace(hour=9, minute=0)
                continue
            
            slot_end = current + timedelta(minutes=duration_minutes)
            
            # Check if slot conflicts with busy times
            is_available = True
            for busy in busy_times:
                busy_start = datetime.fromisoformat(busy['start'].replace('Z', '+00:00'))
                busy_end = datetime.fromisoformat(busy['end'].replace('Z', '+00:00'))
                
                if (current < busy_end) and (slot_end > busy_start):
                    is_available = False
                    break
            
            if is_available and current > now:
                available_slots.append({
                    'start': current.isoformat() + 'Z',
                    'end': slot_end.isoformat() + 'Z',
                    'display': current.strftime('%A, %B %d at %I:%M %p')
                })
            
            current += timedelta(minutes=30)
        
        return available_slots[:10]  # Return first 10 slots
    
    def create_event(self, lead_name: str, lead_email: str, slot_start: str, duration_minutes: int = 30) -> Optional[str]:
        """Create a calendar event and return the event link"""
        try:
            start_time = datetime.fromisoformat(slot_start.replace('Z', '+00:00'))
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': f'Consultation with {lead_name}',
                'description': f'Scheduled consultation with {lead_name} from Forward Horizon.',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'attendees': [
                    {'email': lead_email},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            event_result = self.service.events().insert(
                calendarId=self.calendar_id, 
                body=event,
                sendUpdates='all'
            ).execute()
            
            return event_result.get('htmlLink')
            
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return None
    
    def generate_booking_link(self, lead_id: int) -> str:
        """Generate a booking link for the lead to select a time slot"""
        # This would typically point to your frontend booking page
        base_url = os.getenv('FRONTEND_URL', 'https://theforwardhorizon.com')
        return f"{base_url}/book-meeting?lead_id={lead_id}"