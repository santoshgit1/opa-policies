from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a model for webhook requests
class WebhookEvent(BaseModel):
    ref: str
    commits: list
    repository: dict

# Define a policy update function
def update_policies():
    # Your logic to update policies goes here
    # For example, pulling latest policies from GitHub or reloading policies
    print("Updating policies from GitHub...")

@app.get("/")
def read_root():
    return {"message": "Server is running"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event")

    # Log headers and payload for debugging
    print("Headers:", request.headers)
    print("Received payload:", payload)

    if event_type == "push":
        update_policies()  # Call your policy update logic
        return {"message": "Policies updated"}, 200
    else:
        raise HTTPException(status_code=400, detail="Event type not supported")
    
    return {"message": "Received"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7002)
