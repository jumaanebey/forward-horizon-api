# Add to Forward Horizon Website

Your API is live at: `https://forward-horizon-api.vercel.app`

## Add this JavaScript to your contact form:

```javascript
async function submitLead(event) {
  event.preventDefault();
  
  const formData = new FormData(event.target);
  const name = formData.get('name');
  const email = formData.get('email');
  const phone = formData.get('phone');
  
  try {
    const response = await fetch(`https://forward-horizon-api.vercel.app/api/leads?name=${name}&email=${email}&phone=${phone}`, {
      method: 'POST'
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Show success message
      alert(data.message);
      // Clear form
      event.target.reset();
    }
  } catch (error) {
    console.error('Error submitting lead:', error);
    alert('Sorry, there was an error. Please try again.');
  }
}

// Attach to your form
document.getElementById('contact-form').addEventListener('submit', submitLead);
```

## API Endpoints:

- **Health Check:** GET `https://forward-horizon-api.vercel.app/api/health`
- **Create Lead:** POST `https://forward-horizon-api.vercel.app/api/leads?name=John&email=john@example.com&phone=555-0100`
- **Welcome:** GET `https://forward-horizon-api.vercel.app/api`

## Test with curl:

```bash
curl -X POST "https://forward-horizon-api.vercel.app/api/leads?name=John%20Doe&email=john@example.com&phone=310-488-5280"
```

Your API is fully deployed and working!