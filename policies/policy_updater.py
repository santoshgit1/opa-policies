import logging
from fastapi import FastAPI, Request, HTTPException
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()

# Define the webhook route
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        logger.info(f"Received webhook payload: {payload}")
        print("Received payload:", payload)

        # Example: Check if the push event is present in the payload
        if "push" in payload:
            # Run the git pull command to update the policies
            try:
                result = subprocess.run(
                    ["git", "pull"],
                    cwd="C:/Users/Public/Pictures/SandyDOCS/WorkDocs/Projects/Kumbameela/Other/acm/Other/git/opa-policies",  # Replace with the path to your local repo
                    check=True,
                    text=True,
                    capture_output=True
                )
                logger.info(f"Git pull successful: {result.stdout}")
                return {"status": "success", "output": result.stdout}
            except subprocess.CalledProcessError as e:
                logger.error(f"Git pull failed: {e.output}")
                raise HTTPException(status_code=500, detail=f"Git pull failed: {e.output}")
        else:
            logger.info("Push event not found in payload")
            return {"status": "ignored", "reason": "Event not relevant"}
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"message": "Received"}

# If running this script directly, use Uvicorn to serve the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7002)
