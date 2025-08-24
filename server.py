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
def create_lead(name: str = "Test", email: str = None, phone: str = None):
    return {
        "message": f"Lead {name} created!",
        "name": name,
        "email": email,
        "phone": phone
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)