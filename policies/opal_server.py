from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Example data for policies; replace with your actual policy logic
policies = {
    "work_policy": {
        "id": "work_policy",
        "description": "This is an work policy.",
        "rules": {
            "allow": ["read"],
            "deny": ["write"]
        }
    }
}

# Define a model for policy requests
class PolicyRequest(BaseModel):
    policy_id: str
    action: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the OPAL server"}

@app.get("/policies/{policy_id}")
def get_policy(policy_id: str):
    if policy_id in policies:
        return policies[policy_id]
    else:
        raise HTTPException(status_code=404, detail="Policy not found")

@app.post("/evaluate")
def evaluate_policy(request: PolicyRequest):
    policy = policies.get(request.policy_id)
    if policy:
        if request.action in policy["rules"].get("allow", []):
            return {"result": "allowed"}
        elif request.action in policy["rules"].get("deny", []):
            return {"result": "denied"}
        else:
            return {"result": "unknown action"}
    else:
        raise HTTPException(status_code=404, detail="Policy not found")

# If running this script directly, use Uvicorn to serve the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7002)
