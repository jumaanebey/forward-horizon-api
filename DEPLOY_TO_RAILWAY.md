# Deploy to Railway (Free $5 Trial)

## Step 1: Upload Code to GitHub

1. Go to [github.com/new](https://github.com/new)
2. Create repository named: `forward-horizon-api`
3. Upload these files from `/Users/jumaanebey/Documents/forward-horizon-api/`:
   - All files in `app/` folder
   - `main.py`
   - `requirements.txt`
   - `railway.json`
   - `README.md`

## Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app/new)
2. Click **"Deploy from GitHub repo"**
3. Select your `forward-horizon-api` repository
4. Railway will auto-detect Python and start deploying

## Step 3: Set Environment Variables

In Railway dashboard, go to Variables tab and add:

```
GOOGLE_CALENDAR_ID=primary
FRONTEND_URL=https://theforwardhorizon.com
```

For Google Calendar (optional - only if you want calendar booking):
```
GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"YOUR_CLIENT_ID","client_secret":"YOUR_SECRET"}}
```

## Step 4: Get Your API URL

After deployment, Railway will give you a URL like:
`https://forward-horizon-api-production.up.railway.app`

## Step 5: Test Your API

```bash
# Test health endpoint
curl https://your-api-url.railway.app/health

# Create a test lead
curl -X POST https://your-api-url.railway.app/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Lead","email":"test@example.com","phone":"555-0100","source":"website"}'
```

## Step 6: Add to Forward Horizon Website

Add this to your contact form:

```javascript
const API_URL = 'https://your-api-url.railway.app';

async function submitLead(formData) {
  const response = await fetch(`${API_URL}/leads`, {
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
}
```

## Monthly Cost Estimate

- **API Server**: ~$2-3/month (well within $5 free tier)
- **Database**: SQLite (free, included)
- **Google Calendar**: Free tier (unlimited API calls for personal use)

Your $5 Railway trial should last the entire month!