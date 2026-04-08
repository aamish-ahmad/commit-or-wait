# app.py
from fastapi import FastAPI
from typing import Optional, Dict, Any
import sys
import os

# Ensure Python can find your src folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from rubicon_openenv.environment import RubiconEnvironment

app = FastAPI()

# Initialize your environment
env = RubiconEnvironment(task="easy")

@app.post("/reset")
async def reset_env(payload: Optional[Dict[str, Any]] = None):
    # Grader sends a POST to reset. We absorb the payload and reset the env.
    obs = env.reset()
    return obs

@app.post("/step")
async def step_env(payload: Optional[Dict[str, Any]] = None):
    # Grader sends a POST to step. We extract the action if it exists.
    action = payload.get("action") if payload else None
    
    # Run the step in your environment
    obs, reward, done, info = env.step(action)
    
    # Return the exact JSON structure the RL grader expects
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}