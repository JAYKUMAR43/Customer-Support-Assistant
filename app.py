from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import os

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

# In-memory environment storage
envs: Dict[str, EcommerceEnv] = {
    "Easy": EcommerceEnv(task_level="Easy"),
    "Medium": EcommerceEnv(task_level="Medium"),
    "Hard": EcommerceEnv(task_level="Hard")
}

# Current global active level
active_level = "Easy"

@app.api_route("/reset", methods=["GET", "POST"], response_model=Observation)
async def reset(level: Optional[str] = None):
    """Resets the environment and optionally changes the task difficulty."""
    global active_level
    if level and level in envs:
        active_level = level
    
    return envs[active_level].reset()

@app.post("/step", response_model=StepResponse)
async def step(action: Action):
    """Executes a single step in the environment."""
    try:
        obs, reward, done, info = envs[active_level].step(action)
        return StepResponse(
            observation=obs,
            reward=reward,
            done=done,
            info=info
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state", response_model=State)
async def get_state():
    """Returns the current state of the environment."""
    try:
        return envs[active_level].state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/config")
async def get_config():
    return {
        "active_level": active_level,
        "available_levels": list(envs.keys())
    }

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "OpenEnv Backend API is running",
        "endpoints": ["/reset", "/step", "/state", "/config"]
    }
