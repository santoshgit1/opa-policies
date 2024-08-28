import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the OPAL server"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    print(f"Received payload: {payload}")
    # Further processing here...
    return {"message": "Received"}

@app.get("/policies/{policy_id}")
def get_policy(policy_id: str):
    logger.info(f"Fetching policy {policy_id}")
    if policy_id in policies:
        return policies[policy_id]
    else:
        logger.error(f"Policy {policy_id} not found")
        raise HTTPException(status_code=404, detail="Policy not found")

@app.post("/evaluate")
def evaluate_policy(request: PolicyRequest):
    logger.info(f"Evaluating policy {request.policy_id} with action {request.action}")
    policy = policies.get(request.policy_id)
    if policy:
        if request.action in policy["rules"].get("allow", []):
            result = {"result": "allowed"}
        elif request.action in policy["rules"].get("deny", []):
            result = {"result": "denied"}
        else:
            result = {"result": "unknown action"}
        logger.info(f"Evaluation result: {result}")
        return result
    else:
        logger.error(f"Policy {request.policy_id} not found")
        raise HTTPException(status_code=404, detail="Policy not found")


# If running this script directly, use Uvicorn to serve the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7002)