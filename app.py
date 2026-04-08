from fastapi import FastAPI
from typing import Optional, Dict, Any
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from rubicon_openenv.environment import FraudEnvironment

app = FastAPI()
env = FraudEnvironment()

@app.post("/reset")
async def reset_env(payload: Optional[Dict[str, Any]] = None):
    task = "easy"
    if payload and "task" in payload:
        task = payload["task"]
    obs = env.reset(task)
    return obs

@app.post("/step")
async def step_env(payload: Optional[Dict[str, Any]] = None):
    action_type = "investigate"
    if payload and "action" in payload:
        if isinstance(payload["action"], dict):
            action_type = payload["action"].get("action_type", "investigate")
        else:
            action_type = payload["action"]
            
    result = env.step(action_type)
    return result

@app.get("/state")
async def get_state():
    return env.state()

@app.get("/health")
async def health():
    return {"status": "healthy"}