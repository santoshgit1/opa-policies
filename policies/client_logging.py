import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the OPAL server URL
OPAL_SERVER_URL = "http://localhost:7002"

# Function to fetch a policy
def fetch_policy(policy_id):
    url = f"{OPAL_SERVER_URL}/policies/{policy_id}"
    logger.info(f"Fetching policy from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Policy {policy_id} not found.")
        return None

# Function to evaluate a policy
def evaluate_policy(policy_id, action):
    url = f"{OPAL_SERVER_URL}/evaluate"
    data = {
        "policy_id": policy_id,
        "action": action
    }
    logger.info(f"Evaluating policy with data {data}")
    response = requests.post(url, json=data)
    return response.json()

# Example usage
if __name__ == "__main__":
    policy_id = "work_policy"
    action = "read"
    
    policy = fetch_policy(policy_id)
    if policy:
        logger.info(f"Policy fetched: {policy}")
    
    result = evaluate_policy(policy_id, action)
    logger.info(f"Evaluation result: {result}")
