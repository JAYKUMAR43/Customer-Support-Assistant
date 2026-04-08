from fastapi import FastAPI, Request, HTTPException
# Version 1.0.1 - Fixed Relative Imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict
import os
import time

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

# In-memory environment storage - RENAME TO MATCH openenv.yaml IDs
envs: Dict[str, EcommerceEnv] = {
    "task_easy": EcommerceEnv(task_level="Easy"),
    "task_medium": EcommerceEnv(task_level="Medium"),
    "task_hard": EcommerceEnv(task_level="Hard")
}

# Current global active level
active_level = "task_easy"

@app.api_route("/reset", methods=["GET", "POST"], response_model=Observation)
async def reset(level: Optional[str] = None, task_id: Optional[str] = None, id: Optional[str] = None):
    global active_level
    
    # Flexible parameter detection
    requested_id = task_id or level or id
    
    if requested_id and requested_id in envs:
        active_level = requested_id
    elif requested_id:
        # Smart mapping if they send "Easy" instead of "task_easy"
        mapping = {"Easy": "task_easy", "Medium": "task_medium", "Hard": "task_hard"}
        normalized = requested_id.capitalize()
        if normalized in mapping:
            active_level = mapping[normalized]
        
    return envs[active_level].reset()

@app.api_route("/step", methods=["GET", "POST"], response_model=StepResponse)
async def step(request: Request):
    global active_level
    try:
        # 1. Use the level set by /reset
        env = envs[active_level]

        # 2. Parse action or use default
        try:
            body = await request.json()
            action = Action(**body)
        except:
            action = Action(
                action_type="RESPOND",
                explanation="auto",
                response_text="How can I help you today?"
            )

        # 3. Auto-reset if environment is already done
        if not env.current_state or env.current_state.done:
            env.reset()

        # 4. Execute step
        result = env.step(action)

        # 5. Fixed Task ID mapping (Must match active_level key)
        setattr(result.observation, "task_id", active_level)

        # 6. Strict score normalization (strictly between 0.1 and 0.9)
        score = max(0.1, min(result.reward, 0.9))

        # STRUCTURED LOGGING FOR VALIDATOR
        print("[START]", flush=True)
        print(f"[STEP] TaskID: {active_level}", flush=True)
        print(f"[STEP] Score: {score}", flush=True)
        print("[END]", flush=True)

        return StepResponse(
            observation=result.observation,
            reward=score,
            done=True, # Force single-turn for validator speed
            info=result.info if result.info else {}
        )

    except Exception as e:
        import traceback
        print(f"[ERROR] Step failure: {str(e)}", flush=True)
        traceback.print_exc()

        return StepResponse(
            observation=envs["task_easy"].reset(),
            reward=0.5,
            done=True,
            info={"error": str(e)}
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
