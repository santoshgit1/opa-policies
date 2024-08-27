from fastapi import FastAPI, Request, HTTPException
import subprocess

# Initialize the FastAPI app
app = FastAPI()

# Define the webhook route
@app.post("/webhook")
async def handle_webhook(request: Request):
    # Here, you can process the webhook payload if needed
    payload = await request.json()

    # Example: Check if the push event is present in the payload
    if "push" in payload:
        # Run the git pull command to update the policies
        try:
            result = subprocess.run(
                ["git", "pull"],
                cwd="/path/to/your/local/repo",  # Replace with the path to your local repo
                check=True,
                text=True,
                capture_output=True
            )
            return {"status": "success", "output": result.stdout}
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Git pull failed: {e.output}")
    else:
        return {"status": "ignored", "reason": "Event not relevant"}

# If running this script directly, use Uvicorn to serve the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7002)
