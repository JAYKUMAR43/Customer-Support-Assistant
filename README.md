# AI-Powered E-Commerce Customer Support (Full-Stack OpenEnv)

A production-grade, full-stack reinforcement learning environment for handling e-commerce support queries.

## Features
- **OpenEnv Specification**: Fully compliant with `reset`, `step`, and `state`.
- **Advanced Observation Space**: Includes sentiment analysis and conversation history.
- **Premium React Dashboard**: High-end SaaS-style UI with Framer Motion animations.
- **Nuanced Reward System**: Rewards correct decisions, penalizes fraud, and adds bonuses for sentiment improvement.
- **Multi-Level Tasks**: Easy, Medium, and Hard scenarios ranging from tracking to fraud detection.

## Project Structure
- `backend/`: FastAPI server, environment logic, and models.
- `frontend/`: React dashboard built with Vite and Tailwind CSS.
- `openenv.yaml`: OpenEnv metadata.
- `inference.py`: Baseline agent and evaluation script.
- `Dockerfile`: Multi-stage build for Hugging Face Space deployment.

## Installation & Local Development

### 1. Backend Setup
1. **Install Python Dependencies**
   ```bash
   pip install fastapi uvicorn pydantic requests
   ```
2. **Start Backend**
   ```bash
   python -m uvicorn backend.app:app --reload --port 8000
   ```

### 2. Frontend Setup
1. **Navigate to Frontend**
   ```bash
   cd frontend
   ```
2. **Install Node Dependencies**
   ```bash
   npm install
   ```
3. **Start Frontend**
   ```bash
   npm run dev
   ```

## Deployment on Hugging Face Spaces

1. Create a "Docker" Space on Hugging Face.
2. Ensure the `Dockerfile` is in the project root.
3. Push all files to the Space repository.
4. HF will build and serve the integrated full-stack dashboard on port 7860.

## Baseline Inference Evaluation

Run the evaluation script to verify the environment with an agent simulation:
```bash
python inference.py
```

## Grading System
- **Reward Range**: [-12.0, 15.0]
- **Scenario Scoring**: 
    - Correct Decision: +10
    - Missed Fraud: -12
    - Sentiment Bonus: +3
    - Business Impact: Dynamic calculation based on order value.
