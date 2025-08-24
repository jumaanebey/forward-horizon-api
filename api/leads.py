from fastapi import FastAPI

app = FastAPI()

@app.post("/api/leads")
async def create_lead(name: str, email: str = None, phone: str = None):
    return {
        "success": True,
        "message": f"Thank you {name}! We'll be in touch soon.",
        "data": {
            "name": name,
            "email": email,
            "phone": phone
        }
    }