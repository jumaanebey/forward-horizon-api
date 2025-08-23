# Forward Horizon Lead Funnel API

FastAPI-based lead funnel with Google Calendar integration for automated scheduling and follow-ups.

## Features

- Lead capture and management
- Google Calendar integration for automatic scheduling
- Automated SMS/email follow-ups
- FAQ auto-responses
- Webhook endpoints for inbound messages

## Setup

### 1. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Calendar API
4. Create credentials (OAuth 2.0 for desktop app)
5. Download `credentials.json`

### 2. Environment Variables

Set these in your deployment platform:

```bash
# Google Calendar
GOOGLE_CALENDAR_ID=primary  # or your specific calendar ID
GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"...","client_secret":"..."}}

# Frontend URL for booking links
FRONTEND_URL=https://theforwardhorizon.com

# Optional: Static scheduling URL (fallback)
SCHEDULING_URL=https://calendly.com/your-link
```

### 3. Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway deploy
```

### 4. Add to Forward Horizon Website

Add this JavaScript to your contact forms:

```javascript
// Lead submission
const submitLead = async (formData) => {
  const response = await fetch('https://your-api-url.railway.app/leads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: formData.name,
      email: formData.email,
      phone: formData.phone,
      source: 'website'
    })
  });
  return response.json();
};

// Get available calendar slots
const getAvailableSlots = async () => {
  const response = await fetch('https://your-api-url.railway.app/calendar/available-slots');
  return response.json();
};

// Book a meeting
const bookMeeting = async (leadId, slotStart) => {
  const response = await fetch('https://your-api-url.railway.app/calendar/book-meeting', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      lead_id: leadId,
      slot_start: slotStart
    })
  });
  return response.json();
};
```

## API Endpoints

- `POST /leads` - Create new lead
- `POST /webhooks/inbound` - Handle inbound messages
- `GET /calendar/available-slots` - Get available time slots
- `POST /calendar/book-meeting` - Book a meeting
- `GET /health` - Health check

## Automated Flow

1. **Lead submits form** → API creates lead, sends welcome message
2. **1 hour later** → First follow-up nudge
3. **2 hours later** → Second follow-up nudge  
4. **4 hours later** → Final follow-up, then marked as "cold"
5. **Lead replies "YES"** → Gets booking link with available slots
6. **Lead books meeting** → Calendar event created, confirmations sent