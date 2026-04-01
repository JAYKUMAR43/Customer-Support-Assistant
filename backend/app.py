from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict
import os

from .models import Observation, Action, StepResponse, State
from .env import EcommerceEnv

app = FastAPI(title="AI-Powered E-Commerce Customer Support")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.post("/reset", response_model=Observation)
async def reset(level: Optional[str] = None):
    global active_level
    if level and level in envs:
        active_level = level
    return envs[active_level].reset()

@app.post("/step", response_model=StepResponse)
async def step(action: Action):
    """
    Executes a step in the environment and returns a StepResponse.
    Unpacks the standardized OpenEnv tuple (obs, reward, done, info).
    """
    obs, reward, done, info = envs[active_level].step(action)
    return StepResponse(
        observation=obs,
        reward=reward,
        done=done,
        info=info
    )

@app.get("/state", response_model=State)
async def get_state():
    return envs[active_level].state()

@app.get("/config")
async def get_config():
    return {
        "active_level": active_level,
        "available_levels": list(envs.keys())
    }

# Serving built frontend (HF Space requirement)
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path and os.path.exists(os.path.join(frontend_path, full_path)):
            return FileResponse(os.path.join(frontend_path, full_path))
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    @app.get("/")
    async def fallback():
        return {"status": "Backend running. Frontend not built yet."}
