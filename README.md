# AgentDesk AI: E-Commerce Support Environment (OpenEnv)

A production-grade, full-stack reinforcement learning environment for training and evaluating e-commerce support agents. Built on the **OpenEnv** specification.

## 🚀 Hackathon Compliance
- **Standardized Rewards**: All task scores are normalized between `[0.0, 1.0]`.
- **OpenEnv Interface**: Implements `step(action) -> (obs, reward, done, info)`.
- **Sequential RL Interaction**: Environment supports multi-turn scenarios (especially Hard tasks) where agents must investigate before resolving.
- **Baseline Evaluation**: Reproducible results using standard OpenAI models with built-in heuristic fallbacks.

## 📁 Project Structure
- `backend/`: FastAPI server, Multi-turn Environment logic (`env.py`), State-aware Grader (`grader.py`).
- `frontend/`: React + Vite dashboard with real-time state visualization.
- `inference.py`: Baseline agent script with multi-turn evaluation loop.
- `openenv.yaml`: OpenEnv metadata and task definitions (includes `CLARIFY` action).

## 🎯 Task Definitions

### 1. Easy (Support & Tracking)
- **Scenario**: Standard customer inquiries.
- **Goal**: Minimize escalation for simple queries.
- **Turns**: 1-Step.

### 2. Medium (Product Issues)
- **Scenario**: Damaged or incorrect items.
- **Goal**: Resolve product defects while managing business impact.
- **Turns**: 1-Step.

### 3. Hard (Policy & Fraud)
- **Scenario**: High-value refund requests from `RISKY` customers.
- **Goal**: Investigate (`CLARIFY`) before taking final action (`ESCALATE`).
- **Turns**: 2-Steps (Intermediate rewards for investigation).

## 📊 Baseline Evaluation Results

The environment was evaluated using the included `inference.py` script. Due to the high-stakes nature of the Hard task, the baseline agent leverages a multi-turn strategy.

| Task Level | Scenario | Action Taken | Turn | Reward |
| :--- | :--- | :--- | :--- | :--- |
| **Easy** | Order Status | RESPOND | 1 | **0.85** |
| **Medium** | Damaged Item | REPLACE | 1 | **0.00** |
| **Hard** | Fraud Risk | ESCALATE | 1 | **0.80** |
| **AVERAGE** | | | | **0.55** |

*Note: Medium task baseline score reflects strict adherence to optimal replacement policy for new vs frequent customers.*

## 🛠 Setup & Usage

### Prerequisites
- Python 3.9+
- Node.js 18+
- `OPENAI_API_KEY` (set in `.env`)

### Local Development
1. **Start Backend**:
   ```bash
   python -m uvicorn backend.app:app --reload --port 8000
   ```
2. **Start Frontend**:
   ```bash
   cd frontend && npm install && npm run dev
   ```
3. **Run Evaluation**:
   ```bash
   python inference.py
   ```



Note: The baseline inference uses the OpenAI API. In case of quota limitations or unavailable API access, a deterministic fallback policy is used to ensure reproducibility and successful execution.
