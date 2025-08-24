from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Forward Horizon API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/leads")
def create_lead(name: str, email: str = None, phone: str = None):
    return {
        "message": f"Lead {name} created successfully!",
        "name": name,
        "email": email,
        "phone": phone
    }