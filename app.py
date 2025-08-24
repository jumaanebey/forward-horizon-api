from fastapi import FastAPI
import uvicorn
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)