from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api")
def read_root():
    return {"message": "Forward Horizon API is running!", "status": "operational"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "Forward Horizon Lead Capture"}

@app.post("/api/leads")
async def create_lead(request: Request):
    # Get query parameters from the URL
    query_params = request.query_params
    
    name = query_params.get('name', 'Unknown')
    email = query_params.get('email')
    phone = query_params.get('phone')
    
    # Basic validation
    if not name or name == 'Unknown':
        return JSONResponse(
            status_code=400,
            content={"error": "Name is required"}
        )
    
    return {
        "success": True,
        "message": f"Thank you {name}! Your inquiry has been received. We'll contact you within 24 hours.",
        "lead_data": {
            "name": name,
            "email": email,
            "phone": phone,
            "timestamp": "2025-08-24T02:50:00Z",
            "source": "website"
        }
    }

@app.get("/api/test")
def test_endpoint():
    return {"test": "API is working!", "endpoints": ["/api", "/api/health", "/api/leads", "/api/test"]}

# Handle all HTTP methods for leads endpoint
@app.get("/api/leads")
async def get_leads_info():
    return {
        "info": "Send a POST request with query parameters: name, email, phone",
        "example": "/api/leads?name=John%20Doe&email=john@example.com&phone=555-1234"
    }