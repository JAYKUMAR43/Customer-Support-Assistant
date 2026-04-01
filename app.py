from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json

from models import Observation, Action, StepResponse, State
from env import EcommerceEnv

app = FastAPI(title="E-Commerce AI Support Env")

# Enable CORS for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env_instance = EcommerceEnv(task_level="Easy")

@app.post("/reset", response_model=Observation)
async def reset(level: Optional[str] = "Easy"):
    """Resets the environment and optionally changes the task difficulty."""
    global env_instance
    if level not in ["Easy", "Medium", "Hard"]:
        level = "Easy"
    
    # Re-initialize the environment with the requested difficulty
    env_instance = EcommerceEnv(task_level=level)
    return env_instance.reset()

@app.post("/step", response_model=StepResponse)
async def step(action: Action):
    """Executes a single step in the environment."""
    try:
        return env_instance.step(action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state", response_model=State)
async def get_state():
    """Returns the current state of the environment."""
    try:
        return env_instance.state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "OpenEnv Backend API is running",
        "endpoints": ["/reset", "/step", "/state"]
    }
