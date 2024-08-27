from fastapi import FastAPI, Request, HTTPException
import json
import os
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
    # For example, pull latest policies from GitHub or reloading policies
    print("Updating policies from GitHub...")
    # Implementation depends on your policy storage and retrieval logic

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    # Optionally verify the webhook secret if you set one up
    # secret = request.headers.get("X-Hub-Signature")
    # Verify the signature here if necessary

    # Handle the payload
    event_type = request.headers.get("X-GitHub-Event")
    if event_type == "push":
        update_policies()  # Call your policy update logic
        return {"message": "Policies updated"}, 200
    else:
        raise HTTPException(status_code=400, detail="Event type not supported")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7002)
