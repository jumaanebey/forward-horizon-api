from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
def read_root():
    return {"message": "Forward Horizon API is running!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/leads")
async def create_lead(name: str, email: str = None, phone: str = None):
    # In real app, this would save to database
    return {
        "success": True,
        "message": f"Thank you {name}! We'll be in touch soon.",
        "data": {
            "name": name,
            "email": email,
            "phone": phone
        }
    }